// Copyright 2017 Global Phasing Ltd.

#include <sstream>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include "gemmi/version.hpp"
#include "gemmi/dirwalk.hpp"
#include "gemmi/fileutil.hpp"  // for expand_if_pdb_code

namespace py = pybind11;

void add_symmetry(py::module& m); // sym.cpp
void add_grid(py::module& m); // grid.cpp
void add_unitcell(py::module& m); // unitcell.cpp
void add_hkl(py::module& m); // hkl.cpp
void add_mol(py::module& m); // mol.cpp
void add_cif(py::module& cif); // cif.cpp
void add_read_structure(py::module& m); // read.cpp
void add_cif_read(py::module& cif); // read.cpp
void add_smcif(py::module& cif); // smallmol.cpp
void add_monlib(py::module& cif); // smallmol.cpp

PYBIND11_MODULE(gemmi, mg) {
  mg.doc() = "General MacroMolecular I/O";
  mg.attr("__version__") = GEMMI_VERSION;
  add_symmetry(mg);
  add_grid(mg);
  add_unitcell(mg);
  add_hkl(mg);
  add_mol(mg);
  add_smcif(mg);
  add_monlib(mg);
  add_read_structure(mg);
  py::module cif = mg.def_submodule("cif", "CIF file format");
  add_cif(cif);
  add_cif_read(cif);

  py::class_<gemmi::CifWalk>(mg, "CifWalk")
    .def(py::init<const char*>())
    .def("__iter__", [](gemmi::CifWalk& self) {
        return py::make_iterator(self);
    }, py::keep_alive<0, 1>());
  py::class_<gemmi::CoorFileWalk>(mg, "CoorFileWalk")
    .def(py::init<const char*>())
    .def("__iter__", [](gemmi::CoorFileWalk& self) {
        return py::make_iterator(self);
    }, py::keep_alive<0, 1>());
  mg.def("is_pdb_code", &gemmi::is_pdb_code);
  mg.def("expand_pdb_code_to_path", &gemmi::expand_pdb_code_to_path);
  mg.def("expand_if_pdb_code", &gemmi::expand_if_pdb_code,
         py::arg("code"), py::arg("filetype")='M');
}
