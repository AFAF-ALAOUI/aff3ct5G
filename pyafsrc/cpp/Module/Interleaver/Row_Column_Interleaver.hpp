#ifndef ROW_COLUMN_INTERLEAVER
#define ROW_COLUMN_INTERLEAVER

#include <vector>

#include "Module/Module.hpp"
#include "Tools/Interface/Interface_reset.hpp"

namespace aff3ct
{
namespace module
{
/*!
 * \class Row_Column_Interleaver
 *
 * \brief sets the last segments to zero.
 *
 */
class Row_Column_Interleaver : public Module
{
protected:
	const int E1;
	const int E2;
	const int f;
	const int Qm;
	const int G;
	const int C;

public:
	/*!
	 * \brief Constructor.
	 *
	 */
	Row_Column_Interleaver(const int E1, const int E2, const int f, const int Qm, const int G, const int C);

	/*!
	 * \brief Destructor.
	 */
	virtual ~Row_Column_Interleaver() = default;

protected:
	virtual void _interleave(const int *U_K,  int *V_K, const int frame_id);
	virtual void _deinterleave(const int *V_K,  int *U_K, const int frame_id);
	virtual void _deinterleaveLLR(const float *V_K,  float *U_K, const int frame_id);
};
}
}

#endif /*ROW_COLUMN_INTERLEAVER*/
