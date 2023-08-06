"""
Tests the server compute capabilities.
"""

import numpy as np
import pytest
import requests

import qcfractal.interface as ptl
from qcfractal import testing
from qcfractal.testing import fractal_compute_server


### Tests the compute queue stack
@testing.using_psi4
def test_compute_queue_stack(fractal_compute_server):

    # Build a client
    client = ptl.FractalClient(fractal_compute_server)

    # Add a hydrogen and helium molecule
    hydrogen = ptl.Molecule.from_data([[1, 0, 0, -0.5], [1, 0, 0, 0.5]], dtype="numpy", units="bohr")
    helium = ptl.Molecule.from_data([[2, 0, 0, 0.0]], dtype="numpy", units="bohr")

    hydrogen_mol_id, helium_mol_id = client.add_molecules([hydrogen, helium])

    kw = ptl.models.KeywordSet(**{"values": {"e_convergence": 1.e-8}})
    kw_id = client.add_keywords([kw])[0]

    # Add compute
    compute = {
        "meta": {
            "procedure": "single",
            "driver": "energy",
            "method": "HF",
            "basis": "sto-3g",
            "keywords": kw_id,
            "program": "psi4",
        },
        "data": [hydrogen_mol_id, helium],
    }

    # Ask the server to compute a new computation
    r = client.add_compute("psi4", "HF", "sto-3g", "energy", kw_id, [hydrogen_mol_id, helium])
    assert len(r.ids) == 2

    # Manually handle the compute
    fractal_compute_server.await_results()
    assert len(fractal_compute_server.list_current_tasks()) == 0

    # Query result and check against out manual pul
    results_query = {
        "program": "psi4",
        "molecule": [hydrogen_mol_id, helium_mol_id],
        "method": compute["meta"]["method"],
        "basis": compute["meta"]["basis"]
    }
    results = client.query_results(**results_query, status=None)

    assert len(results) == 2
    for r in results:
        assert r.provenance.creator.lower() == "psi4"
        if r.molecule == hydrogen_mol_id:
            assert pytest.approx(-1.0660263371078127, 1e-5) == r.properties.scf_total_energy
        elif r.molecule == helium_mol_id:
            assert pytest.approx(-2.807913354492941, 1e-5) == r.properties.scf_total_energy
        else:
            raise KeyError("Returned unexpected Molecule ID.")

    assert "RHF Reference" in results[0].get_stdout()


### Tests the compute queue stack
@testing.using_geometric
@testing.using_psi4
def test_procedure_optimization_single(fractal_compute_server):

    # Add a hydrogen molecule
    hydrogen = ptl.Molecule.from_data([[1, 0, 0, -0.672], [1, 0, 0, 0.672]], dtype="numpy", units="bohr")
    client = ptl.FractalClient(fractal_compute_server.get_address(""))
    mol_ret = client.add_molecules([hydrogen])

    kw = ptl.models.KeywordSet(values={"scf_properties": ["quadrupole", "wiberg_lowdin_indices"]})
    kw_id = client.add_keywords([kw])[0]

    # Add compute
    options = {
        "keywords": None,
        "qc_spec": {
            "driver": "gradient",
            "method": "HF",
            "basis": "sto-3g",
            "keywords": kw_id,
            "program": "psi4"
        },
    }

    # Ask the server to compute a new computation
    r = client.add_procedure("optimization", "geometric", options, mol_ret)
    assert len(r.ids) == 1
    compute_key = r.ids[0]

    # Manually handle the compute
    fractal_compute_server.await_results()
    assert len(fractal_compute_server.list_current_tasks()) == 0

    # # Query result and check against out manual pul
    query1 = client.query_procedures(procedure="optimization", program="geometric")
    query2 = client.query_procedures(id=compute_key)

    for query in [query1, query2]:
        assert len(query) == 1
        opt_result = query[0]

        assert isinstance(opt_result.provenance.creator, str)
        assert isinstance(str(opt_result), str)  # Check that repr runs
        assert pytest.approx(-1.117530188962681, 1e-5) == opt_result.get_final_energy()

        # Check pulls
        traj = opt_result.get_trajectory()
        assert len(traj) == len(opt_result.energies)

        assert np.array_equal(opt_result.get_final_molecule().symbols, ["H", "H"])

        # Check individual elements
        for ind in range(len(opt_result.trajectory)):
            # Check keywords went through
            assert traj[ind].provenance.creator.lower() == "psi4"
            assert "SCF QUADRUPOLE XY" in traj[ind].extras["qcvars"]
            assert "WIBERG_LOWDIN_INDICES" in traj[ind].extras["qcvars"]

            # Make sure extra was popped
            assert "_qcfractal_tags" not in traj[ind].extras

            raw_energy = traj[ind].properties.return_energy
            assert pytest.approx(raw_energy, 1.e-5) == opt_result.energies[ind]

        # Check result stdout
        assert "RHF Reference" in traj[0].get_stdout()

        assert opt_result.get_molecular_trajectory()[0].id == opt_result.initial_molecule
        assert opt_result.get_molecular_trajectory()[-1].id == opt_result.final_molecule

        # Check stdout
        assert "internal coordinates" in opt_result.get_stdout()

    # Check that duplicates are caught
    r = client.add_procedure("optimization", "geometric", options, [mol_ret[0]])
    assert len(r.ids) == 1
    assert len(r.existing) == 1


@testing.using_geometric
@testing.using_psi4
def test_procedure_optimization_protocols(fractal_compute_server):

    # Add a hydrogen molecule
    hydrogen = ptl.Molecule.from_data([[1, 0, 0, -0.673], [1, 0, 0, 0.673]], dtype="numpy", units="bohr")
    client = fractal_compute_server.client()

    # Add compute
    options = {
        "keywords": None,
        "qc_spec": {
            "driver": "gradient",
            "method": "HF",
            "basis": "sto-3g",
            "program": "psi4"
        },
        "protocols": {
            "trajectory": "final"
        }
    }

    # Ask the server to compute a new computation
    r = client.add_procedure("optimization", "geometric", options, [hydrogen])
    assert len(r.ids) == 1
    compute_key = r.ids[0]

    # Manually handle the compute
    fractal_compute_server.await_results()
    assert len(fractal_compute_server.list_current_tasks()) == 0

    # # Query result and check against out manual pul
    proc = client.query_procedures(id=r.ids)[0]
    assert proc.status == "COMPLETE"

    assert len(proc.trajectory) == 1
    assert len(proc.energies) > 1
