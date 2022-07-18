#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/iostream.h>

#include <vector>

#include "Module/Filter/Filter.hpp"
#include "Module/Filter/Filter_FIR/Filter_FIR.hpp"
#include "Module/Filter/Filter_FIR/Filter_FIR_ccr/Filter_FIR_ccr.hpp"
#include "Module/Filter/Filter_FIR/Filter_FIR_ccr/Filter_FIR_ccr_fast.hpp"
#include "Module/Filter/Filter_FIR/Filter_FIR_ccr/Root_Raised_Cosine/Filter_root_raised_cosine.hpp"
#include "Module/Filter/Filter_FIR/Filter_FIR_ccr/Farrow/Filter_Farrow_quad.hpp"

#include "Module/Filter/Filter_UPFIR/Filter_UPFIR.hpp"

#include "Module/Source/Source_SEG.hpp"
#include "Module/Filler/Filler.hpp"
#include "Module/Segmentor/Segmentor.hpp"
#include "Module/Puncturer/Puncturer.hpp"
#include "Module/Interleaver/Row_Column_Interleaver.hpp"
#include "Module/Scrambler/Scrambler.hpp"
#include "Module/DBPSK/Modulater.hpp"
#include "Module/LayerMapper/Mapper.hpp"
#include "Module/Allocater/Allocater.hpp"
#include "Module/OFDM/OfdmModulater.hpp"
#include "Module/Encoder/LdpcEncoder.hpp"
#include "Module/Encoder/LdpcEncoder_fast.hpp"
#include "Module/Precoder/Precoder.hpp"

namespace py = pybind11;
using namespace py::literals;
using namespace aff3ct;

// Create a	python module using PYBIND11, here our module will be named pyaf
PYBIND11_MODULE(pyaf, m){
	py::scoped_ostream_redirect stream_cout(
	std::cout,                                // std::ostream&
	py::module_::import("sys").attr("stdout") // Python output
	);
	py::scoped_ostream_redirect stream_cerr(
	std::cerr,                                // std::ostream&
	py::module_::import("sys").attr("stderr") // Python output
	);

	// Import AFF3CT module from py_AFF3CT
	py::object py_aff3ct_module = (py::object) py::module_::import("py_aff3ct").attr("module").attr("Module");

	// Create a submodule, here for source (optionnal)
	py::module_ m_source = m.def_submodule("source");
	py::class_<aff3ct::module::Source_SEG>(m_source,"Source_SEG", py_aff3ct_module)
		.def(py::init<const int, const int>(), "A"_a, "C"_a);

	// Create a submodule, here for filler (optionnal)
	py::module_ m_filler = m.def_submodule("filler");
	py::class_<aff3ct::module::Filler>(m_filler,"Filler", py_aff3ct_module)
		.def(py::init<const int, const int, const int>(), "Kp"_a, "K"_a, "C"_a);

	// Create a submodule, here for segmentor (optionnal)
	py::module_ m_segmentor = m.def_submodule("segmentor");
	py::class_<aff3ct::module::Segmentor>(m_segmentor,"Segmentor", py_aff3ct_module)
	 	.def(py::init<const int, const int>(), "B"_a, "C"_a);

	// Create a submodule, here for Puncturer (optionnal)
	py::module_ m_puncturer = m.def_submodule("puncturer");
	py::class_<aff3ct::module::Puncturer>(m_puncturer,"Puncturer", py_aff3ct_module)
			.def(py::init<const int, const int, const int, const int, const int, const int, const int, const int, const int>(), "C"_a, "Kp"_a, "K"_a, "N"_a, "E1"_a, "E2"_a, "f"_a, "Zc"_a, "stp"_a);

	// Create a submodule, here for Interleaver (optionnal)
	py::module_ m_interleaver = m.def_submodule("interleaver");
	py::class_<aff3ct::module::Row_Column_Interleaver>(m_interleaver,"Row_Column_Interleaver", py_aff3ct_module)
			.def(py::init<const int, const int, const int, const int, const int, const int>(), "E1"_a, "E2"_a, "G"_a, "f"_a, "Qm"_a, "C"_a);

	// Create a submodule, here for filter (optionnal)
	py::module_ m_filter = m.def_submodule("filter");

	// Bind a custom class, here is the binding for the "aff3ct::module::Filter<float>" class.
	// py_aff3ct_module is here to indicate to pybind11 that aff3ct::module exists in py_AFF3CT
	py::class_<aff3ct::module::Filter<float>>(m_filter,"Filter", py_aff3ct_module)
		.def(py::init<const int, const int>(), "N"_a, "N_fil"_a);

	// Bind a custom class, here is the binding for the "aff3ct::module::Filter_FIR<float>" class.
	// aff3ct::module::Filter<float> is here to indicate inheritance
	py::class_<aff3ct::module::Filter_FIR<float>, aff3ct::module::Filter<float>>(m_filter,"Filter_FIR")
		.def(py::init<const int, const std::vector<float>>(), "N"_a, "h"_a);

	// Bind a custom class, here is the binding for the "aff3ct::module::Filter_FIR_ccr<float>" class.
	py::class_<aff3ct::module::Filter_FIR_ccr<float>, aff3ct::module::Filter_FIR<float>>(m_filter,"Filter_FIR_ccr")
		.def(py::init<const int, const std::vector<float>>(), "N"_a, "h"_a);

	// Bind a custom class, here is the binding for the "aff3ct::module::Filter_FIR_ccr_fast<float>" class.
	py::class_<aff3ct::module::Filter_FIR_ccr_fast<float>, aff3ct::module::Filter_FIR_ccr<float>>(m_filter,"Filter_FIR_ccr_fast")
		.def(py::init<const int, const std::vector<float>>(), "N"_a, "h"_a);

	// Bind a custom class, here is the binding for the "aff3ct::module::Filter_root_raised_cosine<float>" class.
	py::class_<aff3ct::module::Filter_root_raised_cosine<float>, aff3ct::module::Filter_FIR_ccr_fast<float>>(m_filter,"Filter_root_raised_cosine")
		.def(py::init<const int,  const float, const int, const int>(), "N"_a, "rolloff"_a = 0.05, "samples_per_symbol"_a = 4, "delay_in_symbol"_a = 50)
		.def_static("synthetize", &aff3ct::module::Filter_root_raised_cosine<float>::synthetize);

	// Bind a custom class, here is the binding for the "aff3ct::module::Filter_UPFIR<float>" class.
	py::class_<aff3ct::module::Filter_UPFIR<float, aff3ct::module::Filter_FIR_ccr>, aff3ct::module::Filter<float>>(m_filter,"Filter_UPFIR")
		.def(py::init<const int, const std::vector<float>, const int>(), "N"_a, "h"_a, "osf"_a = 1);

	// Bind a custom class, here is the binding for the "aff3ct::module::Filter_Farrow_quad<float>" class.
	py::class_<aff3ct::module::Filter_Farrow_quad<float>, aff3ct::module::Filter_FIR_ccr_fast<float>>(m_filter,"Filter_Farrow_quad")
		.def(py::init<const int, const float>(), "N"_a, "mu"_a=0.0);

	// Create a submodule, here for Scrambler (optionnal)
	py::module_ m_scrambler = m.def_submodule("scrambler");
	py::class_<aff3ct::module::Scrambler>(m_scrambler,"Scrambler", py_aff3ct_module)
		.def(py::init<const int, const int>(), "G"_a, "C_init"_a);

	// Create a submodule, here for Modem (optionnal)
	py::module_ m_modulater = m.def_submodule("pi2modulater");
	py::class_<aff3ct::module::Modulater>(m_modulater,"Modulater", py_aff3ct_module)
		.def(py::init<const int, const int>(), "N"_a, "C"_a);

	// Create a submodule, here for Mapper (optionnal)
	py::module_ m_mapper = m.def_submodule("LayerMapper");
	py::class_<aff3ct::module::Mapper>(m_mapper,"Mapper", py_aff3ct_module)
		.def(py::init<const int, const int, const int>(), "N"_a, "Nl"_a, "C"_a);

	// Create a submodule, here for Allocater (optionnal)
	py::module_ m_allocater = m.def_submodule("allocater");
	py::class_<aff3ct::module::Allocater>(m_allocater,"Allocater", py_aff3ct_module)
		.def(py::init<const int, const int, const int, const int, const int, const int, const int, const int, const int, const int, const int, const int>(), "M"_a, "Mgrid"_a, "Na"_a, "Nr"_a, "Nslot"_a, "Nofdms"_a, "Dl"_a, "Msc"_a, "pos1"_a=-1, "pos2"_a=-1, "pos3"_a=-1, "pos4"_a=-1);

	// Create a submodule, here for ofdm (optionnal)
	py::module_ m_ofdm = m.def_submodule("ofdm");
	py::class_<aff3ct::module::OfdmModulater>(m_ofdm,"OfdmModulater", py_aff3ct_module)
		.def(py::init<const int, const int, const int, const int, const int, const int>(), "Mgrid"_a, "Na"_a, "Nr"_a, "Msc"_a, "Nifft"_a, "k0"_a);

	// Create a submodule (optionnal)
	py::module_ m_encoder = m.def_submodule("encoder");
	py::class_<aff3ct::module::LdpcEncoder>(m_encoder,"LdpcEncoder", py_aff3ct_module)
		.def(py::init<const int, const int, const int, const int, const int, const int>(), "K"_a, "N"_a, "BG"_a, "ils"_a, "Zc"_a, "C"_a);

	py::module_ m_encoder_fast = m.def_submodule("encoder");
	py::class_<aff3ct::module::LdpcEncoder_fast>(m_encoder_fast,"LdpcEncoder_fast", py_aff3ct_module)
		.def(py::init<const int, const int, const int, const int, const int, const int>(), "K"_a, "N"_a, "BG"_a, "ils"_a, "Zc"_a, "C"_a);

	py::module_ m_precoder = m.def_submodule("precoder");
	py::class_<aff3ct::module::Precoder>(m_precoder,"Precoder", py_aff3ct_module)
		.def(py::init<const int, const int, const int, const int, const int>(), "Nb"_a, "Nl"_a, "Na"_a, "TPMI"_a, "val"_a);


}
