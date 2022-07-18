#ifndef LDPCENCODER
#define LDPCENCODER

#include <vector>

#include "Module/Module.hpp"
#include "Tools/Interface/Interface_reset.hpp"

namespace aff3ct
{
namespace module
{
/*!
 * \class LdpcEncoder
 *
 * \brief
 */
class LdpcEncoder : public Module
{
protected:
	const int K;     /*!< Bit Length */
	const int N;     /*!< Code Length */
	const int BG;
	const int ils;
	const int Zc;
	const int C;
	std::vector<std::vector<int> > G;


public:
	/*!
	 * \brief Constructor.
	 */
	LdpcEncoder(const int K, const int N, const int BG, const int ils, const int Zc, const int C);

	/*!
	 * \brief Destructor.
	 */
	virtual ~LdpcEncoder() = default;

protected:
	virtual void _encode(const int *U_K,  int *X_N, const int frame_id);
	virtual std::vector<int> _CSRAA(const int Zc, std::vector<int> Gen, const int * vect, const int K, const int N);
	virtual void _MultiplyAdd(std::vector<int>&v, int k, std::vector<int>&r);
};
}
}

#endif /* LdpcEncoder */
