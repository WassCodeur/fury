import numpy as np
import numpy.testing as npt

from fury import molecular as mol, window


def test_periodic_table():
    # Testing class PeriodicTable()
    table = mol.PTable()
    npt.assert_equal(table.atomic_number("C"), 6)
    npt.assert_equal(table.element_name(7), "Nitrogen")
    npt.assert_equal(table.atomic_symbol(8), "O")
    npt.assert_allclose(table.atomic_radius(1, radius_type="VDW"), 1.2, 0.1, 0)
    npt.assert_allclose(table.atomic_radius(6, radius_type="Covalent"), 0.75, 0.1, 0)
    npt.assert_array_almost_equal(table.atom_color(1), np.array([1, 1, 1]))

    # Test errors
    npt.assert_raises(ValueError, table.atomic_radius, 4, radius_type="test")


def get_default_molecular_info(all_info=False):
    atom_numbers = np.array([6, 6, 1, 1, 1, 1, 1, 1])
    atom_coords = np.array(
        [
            [0.5723949486e01, 0.5974463617e01, 0.5898320525e01],
            [0.6840181327e01, 0.6678078649e01, 0.5159998484e01],
            [0.4774278044e01, 0.6499436628e01, 0.5782310182e01],
            [0.5576295333e01, 0.4957554302e01, 0.5530844713e01],
            [0.5926818174e01, 0.5907771848e01, 0.6968386044e01],
            [0.6985130929e01, 0.7695511362e01, 0.5526416671e01],
            [0.7788135127e01, 0.6150201159e01, 0.5277430519e01],
            [0.6632858893e01, 0.6740709254e01, 0.4090898288e01],
        ]
    )
    atom_names = np.array(["CA", "CA", "H", "H", "H", "H", "H", "H"])
    model = np.ones(8)
    residue = np.ones(8)
    chain = np.ones(8) * 65
    is_hetatm = np.ones(8, dtype=bool)
    sheet = []
    helix = []
    if all_info:
        return (
            atom_numbers,
            atom_coords,
            atom_names,
            model,
            residue,
            chain,
            is_hetatm,
            sheet,
            helix,
        )
    return atom_numbers, atom_coords


def test_molecule_creation():
    atomic_numbers, atom_coords = get_default_molecular_info()
    molecule = mol.Molecule(atomic_numbers=atomic_numbers, coords=atom_coords)
    npt.assert_array_almost_equal(mol.get_all_atomic_numbers(molecule), atomic_numbers)
    npt.assert_array_almost_equal(mol.get_all_atomic_positions(molecule), atom_coords)
    npt.assert_equal(molecule.total_num_atoms, 8)
    npt.assert_equal(molecule.total_num_bonds, 0)

    # Test errors
    elements = np.array([6, 6])
    npt.assert_raises(
        ValueError,
        mol.Molecule,
        atomic_numbers=elements,
        coords=atom_coords,
        atom_names=None,
        model=None,
        residue_seq=None,
        chain=None,
        sheet=None,
        helix=None,
        is_hetatm=None,
    )

    elements = list(range(8))
    npt.assert_raises(
        ValueError,
        mol.Molecule,
        atomic_numbers=elements,
        coords=atom_coords,
        atom_names=None,
        model=None,
        residue_seq=None,
        chain=None,
        sheet=None,
        helix=None,
        is_hetatm=None,
    )


def test_add_atom_bond_creation():
    molecule = mol.Molecule()
    mol.add_atom(molecule, 6, 0, 0, 0)
    mol.add_atom(molecule, 6, 1, 0, 0)
    mol.add_bond(molecule, 0, 1, bond_order=1)
    npt.assert_equal(molecule.total_num_bonds, 1)
    npt.assert_equal(molecule.total_num_atoms, 2)


def test_atomic_number():
    # Testing atomic number get/set functions
    molecule = mol.Molecule()
    mol.add_atom(molecule, 4, 0, 0, 0)

    # Testing get_atomic_number
    npt.assert_equal(mol.get_atomic_number(molecule, 0), 4)

    # Testing set_atomic_number
    mol.set_atomic_number(molecule, 0, 6)
    npt.assert_equal(mol.get_atomic_number(molecule, 0), 6)


def test_atomic_position():
    # Testing atomic position get/set functions
    molecule = mol.Molecule()
    mol.add_atom(molecule, 4, 0, 0, 0)

    # Testing get_atomic_position
    npt.assert_array_almost_equal(
        mol.get_atomic_position(molecule, 0), np.array([0, 0, 0])
    )

    # Testing set_atomic_number
    mol.set_atomic_position(molecule, 0, 1, 1, 1)
    npt.assert_array_almost_equal(
        mol.get_atomic_position(molecule, 0), np.array([1, 1, 1])
    )


def test_bond_order():
    # Testing bond order get/set functions

    # Testing get_bond_order
    molecule = mol.Molecule()
    mol.add_atom(molecule, 6, 0, 0, 0)
    mol.add_atom(molecule, 6, 1, 0, 0)
    mol.add_bond(molecule, 0, 1, bond_order=3)
    npt.assert_equal(mol.get_bond_order(molecule, 0), 3)

    # Testing set_bond_order
    mol.set_bond_order(molecule, 0, 2)
    npt.assert_equal(mol.get_bond_order(molecule, 0), 2)

    # Testing get_all_bond_orders
    npt.assert_array_almost_equal(mol.get_all_bond_orders(molecule), np.array([2]))


def test_deep_copy_molecule():
    molecule1 = mol.Molecule()
    mol.add_atom(molecule1, 6, 0, 0, 0)
    mol.add_atom(molecule1, 6, 1, 0, 0)
    mol.add_bond(molecule1, 0, 1, bond_order=1)
    molecule2 = mol.Molecule()
    mol.deep_copy_molecule(molecule2, molecule1)
    npt.assert_equal(molecule2.total_num_bonds, 1)
    npt.assert_equal(molecule2.total_num_atoms, 2)


def test_compute_bonding():
    atomic_numbers, atom_coords = get_default_molecular_info()
    molecule = mol.Molecule(atomic_numbers=atomic_numbers, coords=atom_coords)
    mol.compute_bonding(molecule)
    npt.assert_equal(molecule.total_num_bonds, 7)


def test_sphere_cpk(interactive=False):
    atomic_numbers, atom_coords = get_default_molecular_info()
    molecule = mol.Molecule(atomic_numbers=atomic_numbers, coords=atom_coords)
    table = mol.PTable()
    colormodes = ["discrete", "single"]
    colors = np.array(
        [
            [table.atom_color(1), table.atom_color(6)],
            [[150 / 255, 250 / 255, 150 / 255]],
        ],
        dtype=object,
    )
    scene = window.Scene()
    for i, colormode in enumerate(colormodes):
        test_actor = mol.sphere_cpk(molecule, colormode=colormode)

        scene.add(test_actor)
        scene.reset_camera()
        scene.reset_clipping_range()

        if interactive:
            window.show(scene)

        npt.assert_equal(scene.GetActors().GetNumberOfItems(), 1)

        arr = window.snapshot(scene)
        report = window.analyze_snapshot(arr, colors=colors[i])
        npt.assert_equal(report.objects, 1)
        scene.clear()

    # Testing warnings
    npt.assert_warns(UserWarning, mol.sphere_cpk, molecule, colormode="multiple")


def test_bstick(interactive=False):
    molecule = mol.Molecule()
    mol.add_atom(molecule, 6, 0, 0, 0)
    mol.add_atom(molecule, 6, 2, 0, 0)

    # Test errors for inadequate bonding data
    npt.assert_raises(
        ValueError,
        mol.ball_stick,
        molecule,
        colormode="discrete",
        atom_scale_factor=0.3,
        bond_thickness=0.1,
        multiple_bonds=True,
    )

    mol.add_bond(molecule, 0, 1, bond_order=1)
    colormodes = ["discrete", "single"]
    atom_scale_factor = [0.3, 0.4]
    bond_thickness = [0.1, 0.2]
    multiple_bonds = [True, False]
    table = mol.PTable()
    colors = np.array(
        [
            [table.atom_color(6)],
            [[150 / 255, 150 / 255, 150 / 255], [50 / 255, 50 / 255, 50 / 255]],
        ],
        dtype=object,
    )
    scene = window.Scene()
    for i, colormode in enumerate(colormodes):
        test_actor = mol.ball_stick(
            molecule,
            colormode=colormode,
            atom_scale_factor=atom_scale_factor[i],
            bond_thickness=bond_thickness[i],
            multiple_bonds=multiple_bonds[i],
        )
        scene.add(test_actor)
        scene.reset_camera()
        scene.reset_clipping_range()

        if interactive:
            window.show(scene)

        npt.assert_equal(scene.GetActors().GetNumberOfItems(), 1)

        arr = window.snapshot(scene)
        report = window.analyze_snapshot(arr, colors=colors[i])
        npt.assert_equal(report.objects, 1)
        scene.clear()

    # Testing warnings
    npt.assert_warns(
        UserWarning,
        mol.ball_stick,
        molecule,
        colormode="multiple",
        atom_scale_factor=0.3,
        bond_thickness=0.1,
        multiple_bonds=True,
    )


def test_stick(interactive=False):
    molecule = mol.Molecule()
    mol.add_atom(molecule, 6, 0, 0, 0)
    mol.add_atom(molecule, 6, 2, 0, 0)

    # Test errors for inadequate bonding data
    npt.assert_raises(
        ValueError, mol.stick, molecule, colormode="discrete", bond_thickness=0.1
    )
    mol.add_bond(molecule, 0, 1, bond_order=1)

    colormodes = ["discrete", "single"]
    bond_thickness = [0.1, 0.12]
    table = mol.PTable()
    colors = np.array(
        [
            [table.atom_color(6)],
            [[150 / 255, 150 / 255, 150 / 255], [50 / 255, 50 / 255, 50 / 255]],
        ],
        dtype=object,
    )
    scene = window.Scene()
    for i, colormode in enumerate(colormodes):
        test_actor = mol.stick(
            molecule,
            colormode=colormode,
            bond_thickness=bond_thickness[i],
        )
        scene.add(test_actor)
        scene.reset_camera()
        scene.reset_clipping_range()

        if interactive:
            window.show(scene)

        npt.assert_equal(scene.GetActors().GetNumberOfItems(), 1)

        arr = window.snapshot(scene)
        report = window.analyze_snapshot(arr, colors=colors[i])
        npt.assert_equal(report.objects, 1)
        scene.clear()

    # Testing warnings
    npt.assert_warns(
        UserWarning, mol.stick, molecule, colormode="multiple", bond_thickness=0.1
    )


def test_ribbon(interactive=False):
    scene = window.Scene()

    # Testing if helices and sheets are rendered properly
    atom_coords = np.array(
        [
            [31.726, 105.084, 71.456],
            [31.477, 105.680, 70.156],
            [32.599, 106.655, 69.845],
            [32.634, 107.264, 68.776],
            [30.135, 106.407, 70.163],
            [29.053, 105.662, 70.913],
            [28.118, 106.591, 71.657],
            [28.461, 107.741, 71.938],
            [26.928, 106.097, 71.983],
            [33.507, 106.802, 70.804],
            [34.635, 107.689, 70.622],
            [35.687, 107.018, 69.765],
            [36.530, 107.689, 69.174],
            [35.631, 105.690, 69.688],
            [36.594, 104.921, 68.903],
            [36.061, 104.498, 67.534],
            [36.601, 103.580, 66.916],
            [37.047, 103.645, 69.660],
            [35.907, 102.828, 69.957],
            [37.751, 104.014, 70.958],
        ]
    )
    elements = np.array([7, 6, 6, 8, 6, 6, 6, 8, 7, 7, 6, 6, 8, 7, 6, 6, 8, 6, 8, 6])
    atom_names = np.array(
        [
            "N",
            "CA",
            "C",
            "O",
            "CB",
            "CG",
            "CD",
            "OE1",
            "NE2",
            "N",
            "CA",
            "C",
            "O",
            "N",
            "CA",
            "C",
            "O",
            "CB",
            "OG1",
            "OG2",
        ]
    )
    model = np.ones(20)
    chain = np.ones(20) * 65
    residue_seq = np.ones(20)
    residue_seq[9:13] = 2
    residue_seq[13:] = 3
    residue_seq[6] = 4
    is_hetatm = np.zeros(20, dtype=bool)
    secondary_structure = np.array([[65, 1, 65, 3]])
    colors = np.array([[240 / 255, 0, 128 / 255], [1, 1, 0]])
    for i, color in enumerate(colors):
        if i:
            helix = []
            sheet = secondary_structure
        else:
            helix = secondary_structure
            sheet = []
        molecule = mol.Molecule(
            atomic_numbers=elements,
            coords=atom_coords,
            atom_names=atom_names,
            model=model,
            residue_seq=residue_seq,
            chain=chain,
            sheet=sheet,
            helix=helix,
            is_hetatm=is_hetatm,
        )
        test_actor = mol.ribbon(molecule)
        scene.set_camera(
            position=(28, 113, 74),
            focal_point=(34, 106, 70),
            view_up=(-0.37, 0.29, -0.88),
        )
        scene.add(test_actor)
        scene.reset_camera()
        scene.reset_clipping_range()

        if interactive:
            window.show(scene)
        npt.assert_equal(scene.GetActors().GetNumberOfItems(), 1)
        arr = window.snapshot(scene)
        report = window.analyze_snapshot(arr, colors=[color])
        npt.assert_equal(report.objects, 1)
        scene.clear()


def test_bounding_box(interactive=False):
    scene = window.Scene()
    molecule = mol.Molecule()
    mol.add_atom(molecule, 6, 0, 0, 0)
    mol.add_atom(molecule, 6, 1, 1, 1)
    mol.add_bond(molecule, 0, 1, bond_order=1)

    molecule_actor = mol.stick(molecule)
    test_box = mol.bounding_box(molecule, colors=(0, 1, 1), linewidth=0.1)
    scene.add(molecule_actor)
    scene.add(test_box)

    if interactive:
        window.show(scene)

    npt.assert_equal(scene.GetActors().GetNumberOfItems(), 2)

    table = mol.PTable()
    colors = np.array([table.atom_color(1), table.atom_color(6)])
    arr = window.snapshot(scene)
    report = window.analyze_snapshot(arr, colors=colors)
    npt.assert_equal(report.objects, 1)
    scene.clear()
