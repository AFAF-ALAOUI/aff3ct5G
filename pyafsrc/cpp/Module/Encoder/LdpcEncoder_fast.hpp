#ifndef LDPCENCODERFAST
#define LDPCENCODERFAST

#include <vector>

#include "Module/Module.hpp"
#include "Tools/Interface/Interface_reset.hpp"

namespace aff3ct
{
namespace module
{
/*!
 * \class LdpcEncoder_fast
 *
 * \brief
 */
class LdpcEncoder_fast : public Module
{
protected:
	const int K;     /*!< Bit Length */
	const int N;     /*!< Code Length */
	const int BG;
	const int ils;
	const int Zc;
	const int C;
	std::vector<std::vector<int> > G;
	std::vector<std::vector<int> > Rot;


public:
	/*!
	 * \brief Constructor.
	 */
	LdpcEncoder_fast(const int K, const int N, const int BG, const int ils, const int Zc, const int C);

	/*!
	 * \brief Destructor.
	 */
	virtual ~LdpcEncoder_fast() = default;

protected:
	virtual void _encode(const int *U_K,  int *X_N, const int frame_id);
	virtual std::vector<int> _CSRAA(const int * vect, const int beg);
	virtual std::vector<int> _findItems(std::vector<int> v, int target);
};
}
}

#endif /* LdpcEncoder_fast */
