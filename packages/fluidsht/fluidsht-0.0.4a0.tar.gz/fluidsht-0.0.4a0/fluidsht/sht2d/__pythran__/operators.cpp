#include <pythonic/core.hpp>
#include <pythonic/python/core.hpp>
#include <pythonic/types/bool.hpp>
#include <pythonic/types/int.hpp>
#ifdef _OPENMP
#include <omp.h>
#endif
#include <pythonic/include/types/bool.hpp>
#include <pythonic/include/types/complex128.hpp>
#include <pythonic/include/types/ndarray.hpp>
#include <pythonic/include/types/int.hpp>
#include <pythonic/include/types/NoneType.hpp>
#include <pythonic/include/types/float64.hpp>
#include <pythonic/types/int.hpp>
#include <pythonic/types/ndarray.hpp>
#include <pythonic/types/bool.hpp>
#include <pythonic/types/complex128.hpp>
#include <pythonic/types/NoneType.hpp>
#include <pythonic/types/float64.hpp>
#include <pythonic/include/__builtin__/False.hpp>
#include <pythonic/include/__builtin__/None.hpp>
#include <pythonic/include/__builtin__/complex.hpp>
#include <pythonic/include/__builtin__/pythran/is_none.hpp>
#include <pythonic/include/__builtin__/pythran/static_if.hpp>
#include <pythonic/include/__builtin__/tuple.hpp>
#include <pythonic/include/numpy/empty.hpp>
#include <pythonic/include/operator_/mul.hpp>
#include <pythonic/include/types/slice.hpp>
#include <pythonic/include/types/str.hpp>
#include <pythonic/__builtin__/False.hpp>
#include <pythonic/__builtin__/None.hpp>
#include <pythonic/__builtin__/complex.hpp>
#include <pythonic/__builtin__/pythran/is_none.hpp>
#include <pythonic/__builtin__/pythran/static_if.hpp>
#include <pythonic/__builtin__/tuple.hpp>
#include <pythonic/numpy/empty.hpp>
#include <pythonic/operator_/mul.hpp>
#include <pythonic/types/slice.hpp>
#include <pythonic/types/str.hpp>
namespace __pythran_operators
{
  struct $isstatic7
  {
    typedef void callable;
    typedef void pure;
    template <typename argument_type0 , typename argument_type1 >
    struct type
    {
      typedef typename std::remove_cv<typename std::remove_reference<argument_type1>::type>::type __type0;
      typedef typename pythonic::returnable<decltype(pythonic::types::make_tuple(std::declval<__type0>()))>::type result_type;
    }  
    ;
    template <typename argument_type0 , typename argument_type1 >
    typename type<argument_type0, argument_type1>::result_type operator()(argument_type0&& self_nlm, argument_type1&& uR_lm) const
    ;
  }  ;
  struct $isstatic6
  {
    typedef void callable;
    typedef void pure;
    template <typename argument_type0 , typename argument_type1 >
    struct type
    {
      typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::numpy::functor::empty{})>::type>::type __type0;
      typedef typename std::remove_cv<typename std::remove_reference<argument_type0>::type>::type __type1;
      typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::__builtin__::functor::complex{})>::type>::type __type2;
      typedef decltype(std::declval<__type0>()(std::declval<__type1>(), std::declval<__type2>())) __type3;
      typedef typename pythonic::returnable<decltype(pythonic::types::make_tuple(std::declval<__type3>()))>::type result_type;
    }  
    ;
    template <typename argument_type0 , typename argument_type1 >
    typename type<argument_type0, argument_type1>::result_type operator()(argument_type0&& self_nlm, argument_type1&& uR_lm) const
    ;
  }  ;
  struct $isstatic5
  {
    typedef void callable;
    typedef void pure;
    template <typename argument_type0 , typename argument_type1 >
    struct type
    {
      typedef typename std::remove_cv<typename std::remove_reference<argument_type1>::type>::type __type0;
      typedef typename pythonic::returnable<decltype(pythonic::types::make_tuple(std::declval<__type0>()))>::type result_type;
    }  
    ;
    template <typename argument_type0 , typename argument_type1 >
    typename type<argument_type0, argument_type1>::result_type operator()(argument_type0&& self_nlm, argument_type1&& uD_lm) const
    ;
  }  ;
  struct $isstatic4
  {
    typedef void callable;
    typedef void pure;
    template <typename argument_type0 , typename argument_type1 >
    struct type
    {
      typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::numpy::functor::empty{})>::type>::type __type0;
      typedef typename std::remove_cv<typename std::remove_reference<argument_type0>::type>::type __type1;
      typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::__builtin__::functor::complex{})>::type>::type __type2;
      typedef decltype(std::declval<__type0>()(std::declval<__type1>(), std::declval<__type2>())) __type3;
      typedef typename pythonic::returnable<decltype(pythonic::types::make_tuple(std::declval<__type3>()))>::type result_type;
    }  
    ;
    template <typename argument_type0 , typename argument_type1 >
    typename type<argument_type0, argument_type1>::result_type operator()(argument_type0&& self_nlm, argument_type1&& uD_lm) const
    ;
  }  ;
  struct $isstatic3
  {
    typedef void callable;
    typedef void pure;
    template <typename argument_type0 , typename argument_type1 >
    struct type
    {
      typedef typename std::remove_cv<typename std::remove_reference<argument_type0>::type>::type __type0;
      typedef typename pythonic::returnable<decltype(pythonic::types::make_tuple(std::declval<__type0>()))>::type result_type;
    }  
    ;
    template <typename argument_type0 , typename argument_type1 >
    typename type<argument_type0, argument_type1>::result_type operator()(argument_type0&& rot_lm, argument_type1&& self_nlm) const
    ;
  }  ;
  struct $isstatic2
  {
    typedef void callable;
    typedef void pure;
    template <typename argument_type0 , typename argument_type1 >
    struct type
    {
      typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::numpy::functor::empty{})>::type>::type __type0;
      typedef typename std::remove_cv<typename std::remove_reference<argument_type1>::type>::type __type1;
      typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::__builtin__::functor::complex{})>::type>::type __type2;
      typedef decltype(std::declval<__type0>()(std::declval<__type1>(), std::declval<__type2>())) __type3;
      typedef typename pythonic::returnable<decltype(pythonic::types::make_tuple(std::declval<__type3>()))>::type result_type;
    }  
    ;
    template <typename argument_type0 , typename argument_type1 >
    typename type<argument_type0, argument_type1>::result_type operator()(argument_type0&& rot_lm, argument_type1&& self_nlm) const
    ;
  }  ;
  struct $isstatic1
  {
    typedef void callable;
    typedef void pure;
    template <typename argument_type0 , typename argument_type1 >
    struct type
    {
      typedef typename std::remove_cv<typename std::remove_reference<argument_type0>::type>::type __type0;
      typedef typename pythonic::returnable<decltype(pythonic::types::make_tuple(std::declval<__type0>()))>::type result_type;
    }  
    ;
    template <typename argument_type0 , typename argument_type1 >
    typename type<argument_type0, argument_type1>::result_type operator()(argument_type0&& div_lm, argument_type1&& self_nlm) const
    ;
  }  ;
  struct $isstatic0
  {
    typedef void callable;
    typedef void pure;
    template <typename argument_type0 , typename argument_type1 >
    struct type
    {
      typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::numpy::functor::empty{})>::type>::type __type0;
      typedef typename std::remove_cv<typename std::remove_reference<argument_type1>::type>::type __type1;
      typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::__builtin__::functor::complex{})>::type>::type __type2;
      typedef decltype(std::declval<__type0>()(std::declval<__type1>(), std::declval<__type2>())) __type3;
      typedef typename pythonic::returnable<decltype(pythonic::types::make_tuple(std::declval<__type3>()))>::type result_type;
    }  
    ;
    template <typename argument_type0 , typename argument_type1 >
    typename type<argument_type0, argument_type1>::result_type operator()(argument_type0&& div_lm, argument_type1&& self_nlm) const
    ;
  }  ;
  struct __transonic__
  {
    typedef void callable;
    typedef void pure;
    struct type
    {
      typedef pythonic::types::str __type0;
      typedef typename pythonic::returnable<decltype(pythonic::types::make_tuple(std::declval<__type0>()))>::type result_type;
    }  ;
    typename type::result_type operator()() const;
    ;
  }  ;
  struct __code_new_method__OperatorsSphereHarmo2D__vsh_from_divrotsh
  {
    typedef void callable;
    typedef void pure;
    struct type
    {
      typedef typename pythonic::returnable<pythonic::types::str>::type result_type;
    }  ;
    typename type::result_type operator()() const;
    ;
  }  ;
  struct __code_new_method__OperatorsSphereHarmo2D__divrotsh_from_vsh
  {
    typedef void callable;
    typedef void pure;
    struct type
    {
      typedef typename pythonic::returnable<pythonic::types::str>::type result_type;
    }  ;
    typename type::result_type operator()() const;
    ;
  }  ;
  struct __code_new_method__OperatorsSphereHarmo2D__invlaplacian_sh
  {
    typedef void callable;
    typedef void pure;
    struct type
    {
      typedef typename pythonic::returnable<pythonic::types::str>::type result_type;
    }  ;
    typename type::result_type operator()() const;
    ;
  }  ;
  struct __for_method__OperatorsSphereHarmo2D__invlaplacian_sh
  {
    typedef void callable;
    typedef void pure;
    template <typename argument_type0 , typename argument_type1 , typename argument_type2 = bool>
    struct type
    {
      typedef typename std::remove_cv<typename std::remove_reference<argument_type0>::type>::type __type0;
      typedef typename std::remove_cv<typename std::remove_reference<argument_type1>::type>::type __type1;
      typedef decltype((pythonic::operator_::mul(std::declval<__type0>(), std::declval<__type1>()))) __type2;
      typedef decltype((-std::declval<__type0>())) __type3;
      typedef decltype((pythonic::operator_::mul(std::declval<__type3>(), std::declval<__type1>()))) __type4;
      typedef typename pythonic::returnable<typename __combined<__type2,__type4>::type>::type result_type;
    }  
    ;
    template <typename argument_type0 , typename argument_type1 , typename argument_type2 = bool>
    typename type<argument_type0, argument_type1, argument_type2>::result_type operator()(argument_type0&& self_inv_K2_not0, argument_type1&& a_lm, argument_type2 negative= pythonic::__builtin__::False) const
    ;
  }  ;
  struct __code_new_method__OperatorsSphereHarmo2D__laplacian_sh
  {
    typedef void callable;
    typedef void pure;
    struct type
    {
      typedef typename pythonic::returnable<pythonic::types::str>::type result_type;
    }  ;
    typename type::result_type operator()() const;
    ;
  }  ;
  struct __for_method__OperatorsSphereHarmo2D__laplacian_sh
  {
    typedef void callable;
    typedef void pure;
    template <typename argument_type0 , typename argument_type1 , typename argument_type2 = bool>
    struct type
    {
      typedef typename std::remove_cv<typename std::remove_reference<argument_type0>::type>::type __type0;
      typedef typename std::remove_cv<typename std::remove_reference<argument_type1>::type>::type __type1;
      typedef decltype((pythonic::operator_::mul(std::declval<__type0>(), std::declval<__type1>()))) __type2;
      typedef decltype((-std::declval<__type0>())) __type3;
      typedef decltype((pythonic::operator_::mul(std::declval<__type3>(), std::declval<__type1>()))) __type4;
      typedef typename pythonic::returnable<typename __combined<__type2,__type4>::type>::type result_type;
    }  
    ;
    template <typename argument_type0 , typename argument_type1 , typename argument_type2 = bool>
    typename type<argument_type0, argument_type1, argument_type2>::result_type operator()(argument_type0&& self_K2, argument_type1&& a_lm, argument_type2 negative= pythonic::__builtin__::False) const
    ;
  }  ;
  struct __for_method__OperatorsSphereHarmo2D__vsh_from_divrotsh
  {
    typedef void callable;
    ;
    template <typename argument_type0 , typename argument_type1 , typename argument_type2 , typename argument_type3 , typename argument_type4 = pythonic::types::none_type, typename argument_type5 = pythonic::types::none_type>
    struct type
    {
      typedef typename std::remove_cv<typename std::remove_reference<argument_type5>::type>::type __type0;
      typedef typename std::remove_cv<typename std::remove_reference<argument_type4>::type>::type __type1;
      typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::__builtin__::pythran::functor::static_if{})>::type>::type __type2;
      typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::__builtin__::pythran::functor::is_none{})>::type>::type __type3;
      typedef typename pythonic::assignable<typename std::remove_cv<typename std::remove_reference<argument_type4>::type>::type>::type __type4;
      typedef decltype(std::declval<__type3>()(std::declval<__type4>())) __type5;
      typedef $isstatic4 __type6;
      typedef $isstatic5 __type7;
      typedef decltype(std::declval<__type2>()(std::declval<__type5>(), std::declval<__type6>(), std::declval<__type7>())) __type8;
      typedef typename std::remove_cv<typename std::remove_reference<argument_type1>::type>::type __type9;
      typedef typename pythonic::assignable<decltype(std::declval<__type8>()(std::declval<__type9>(), std::declval<__type4>()))>::type __type10;
      typedef typename pythonic::assignable<typename std::tuple_element<0,typename std::remove_reference<__type10>::type>::type>::type __type11;
      typedef typename std::remove_cv<typename std::remove_reference<argument_type2>::type>::type __type12;
      typedef decltype((-std::declval<__type12>())) __type13;
      typedef typename std::remove_cv<typename std::remove_reference<argument_type0>::type>::type __type14;
      typedef decltype((pythonic::operator_::mul(std::declval<__type13>(), std::declval<__type14>()))) __type15;
      typedef typename __combined<__type11,__type15>::type __type16;
      typedef typename pythonic::assignable<typename std::remove_cv<typename std::remove_reference<argument_type5>::type>::type>::type __type17;
      typedef decltype(std::declval<__type3>()(std::declval<__type17>())) __type18;
      typedef $isstatic6 __type19;
      typedef $isstatic7 __type20;
      typedef decltype(std::declval<__type2>()(std::declval<__type18>(), std::declval<__type19>(), std::declval<__type20>())) __type21;
      typedef typename pythonic::assignable<decltype(std::declval<__type21>()(std::declval<__type9>(), std::declval<__type17>()))>::type __type22;
      typedef typename pythonic::assignable<typename std::tuple_element<0,typename std::remove_reference<__type22>::type>::type>::type __type23;
      typedef typename std::remove_cv<typename std::remove_reference<argument_type3>::type>::type __type24;
      typedef decltype((pythonic::operator_::mul(std::declval<__type24>(), std::declval<__type14>()))) __type25;
      typedef typename __combined<__type23,__type25>::type __type26;
      typedef __type0 __ptype0;
      typedef __type1 __ptype1;
      typedef typename pythonic::returnable<decltype(pythonic::types::make_tuple(std::declval<__type16>(), std::declval<__type26>()))>::type result_type;
    }  
    ;
    template <typename argument_type0 , typename argument_type1 , typename argument_type2 , typename argument_type3 , typename argument_type4 = pythonic::types::none_type, typename argument_type5 = pythonic::types::none_type>
    typename type<argument_type0, argument_type1, argument_type2, argument_type3, argument_type4, argument_type5>::result_type operator()(argument_type0&& self_inv_K2_r, argument_type1&& self_nlm, argument_type2&& div_lm, argument_type3&& rot_lm, argument_type4 uD_lm= pythonic::__builtin__::None, argument_type5 uR_lm= pythonic::__builtin__::None) const
    ;
  }  ;
  struct __for_method__OperatorsSphereHarmo2D__divrotsh_from_vsh
  {
    typedef void callable;
    ;
    template <typename argument_type0 , typename argument_type1 , typename argument_type2 , typename argument_type3 , typename argument_type4 = pythonic::types::none_type, typename argument_type5 = pythonic::types::none_type>
    struct type
    {
      typedef typename std::remove_cv<typename std::remove_reference<argument_type5>::type>::type __type0;
      typedef typename std::remove_cv<typename std::remove_reference<argument_type4>::type>::type __type1;
      typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::__builtin__::pythran::functor::static_if{})>::type>::type __type2;
      typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::__builtin__::pythran::functor::is_none{})>::type>::type __type3;
      typedef typename pythonic::assignable<typename std::remove_cv<typename std::remove_reference<argument_type4>::type>::type>::type __type4;
      typedef decltype(std::declval<__type3>()(std::declval<__type4>())) __type5;
      typedef $isstatic0 __type6;
      typedef $isstatic1 __type7;
      typedef decltype(std::declval<__type2>()(std::declval<__type5>(), std::declval<__type6>(), std::declval<__type7>())) __type8;
      typedef typename std::remove_cv<typename std::remove_reference<argument_type1>::type>::type __type9;
      typedef typename pythonic::assignable<decltype(std::declval<__type8>()(std::declval<__type4>(), std::declval<__type9>()))>::type __type10;
      typedef typename pythonic::assignable<typename std::tuple_element<0,typename std::remove_reference<__type10>::type>::type>::type __type11;
      typedef typename std::remove_cv<typename std::remove_reference<argument_type0>::type>::type __type12;
      typedef decltype((-std::declval<__type12>())) __type13;
      typedef typename std::remove_cv<typename std::remove_reference<argument_type2>::type>::type __type14;
      typedef decltype((pythonic::operator_::mul(std::declval<__type13>(), std::declval<__type14>()))) __type15;
      typedef typename __combined<__type11,__type15>::type __type16;
      typedef typename pythonic::assignable<typename std::remove_cv<typename std::remove_reference<argument_type5>::type>::type>::type __type17;
      typedef decltype(std::declval<__type3>()(std::declval<__type17>())) __type18;
      typedef $isstatic2 __type19;
      typedef $isstatic3 __type20;
      typedef decltype(std::declval<__type2>()(std::declval<__type18>(), std::declval<__type19>(), std::declval<__type20>())) __type21;
      typedef typename pythonic::assignable<decltype(std::declval<__type21>()(std::declval<__type17>(), std::declval<__type9>()))>::type __type22;
      typedef typename pythonic::assignable<typename std::tuple_element<0,typename std::remove_reference<__type22>::type>::type>::type __type23;
      typedef typename std::remove_cv<typename std::remove_reference<argument_type3>::type>::type __type24;
      typedef decltype((pythonic::operator_::mul(std::declval<__type12>(), std::declval<__type24>()))) __type25;
      typedef typename __combined<__type23,__type25>::type __type26;
      typedef __type0 __ptype2;
      typedef __type1 __ptype3;
      typedef typename pythonic::returnable<decltype(pythonic::types::make_tuple(std::declval<__type16>(), std::declval<__type26>()))>::type result_type;
    }  
    ;
    template <typename argument_type0 , typename argument_type1 , typename argument_type2 , typename argument_type3 , typename argument_type4 = pythonic::types::none_type, typename argument_type5 = pythonic::types::none_type>
    typename type<argument_type0, argument_type1, argument_type2, argument_type3, argument_type4, argument_type5>::result_type operator()(argument_type0&& self_K2_r, argument_type1&& self_nlm, argument_type2&& uD_lm, argument_type3&& uR_lm, argument_type4 div_lm= pythonic::__builtin__::None, argument_type5 rot_lm= pythonic::__builtin__::None) const
    ;
  }  ;
  template <typename argument_type0 , typename argument_type1 >
  typename $isstatic7::type<argument_type0, argument_type1>::result_type $isstatic7::operator()(argument_type0&& self_nlm, argument_type1&& uR_lm) const
  {
    return pythonic::types::make_tuple(uR_lm);
  }
  template <typename argument_type0 , typename argument_type1 >
  typename $isstatic6::type<argument_type0, argument_type1>::result_type $isstatic6::operator()(argument_type0&& self_nlm, argument_type1&& uR_lm) const
  {
    ;
    ;
    return pythonic::types::make_tuple(pythonic::numpy::functor::empty{}(self_nlm, pythonic::__builtin__::functor::complex{}));
  }
  template <typename argument_type0 , typename argument_type1 >
  typename $isstatic5::type<argument_type0, argument_type1>::result_type $isstatic5::operator()(argument_type0&& self_nlm, argument_type1&& uD_lm) const
  {
    return pythonic::types::make_tuple(uD_lm);
  }
  template <typename argument_type0 , typename argument_type1 >
  typename $isstatic4::type<argument_type0, argument_type1>::result_type $isstatic4::operator()(argument_type0&& self_nlm, argument_type1&& uD_lm) const
  {
    ;
    ;
    return pythonic::types::make_tuple(pythonic::numpy::functor::empty{}(self_nlm, pythonic::__builtin__::functor::complex{}));
  }
  template <typename argument_type0 , typename argument_type1 >
  typename $isstatic3::type<argument_type0, argument_type1>::result_type $isstatic3::operator()(argument_type0&& rot_lm, argument_type1&& self_nlm) const
  {
    return pythonic::types::make_tuple(rot_lm);
  }
  template <typename argument_type0 , typename argument_type1 >
  typename $isstatic2::type<argument_type0, argument_type1>::result_type $isstatic2::operator()(argument_type0&& rot_lm, argument_type1&& self_nlm) const
  {
    ;
    ;
    return pythonic::types::make_tuple(pythonic::numpy::functor::empty{}(self_nlm, pythonic::__builtin__::functor::complex{}));
  }
  template <typename argument_type0 , typename argument_type1 >
  typename $isstatic1::type<argument_type0, argument_type1>::result_type $isstatic1::operator()(argument_type0&& div_lm, argument_type1&& self_nlm) const
  {
    return pythonic::types::make_tuple(div_lm);
  }
  template <typename argument_type0 , typename argument_type1 >
  typename $isstatic0::type<argument_type0, argument_type1>::result_type $isstatic0::operator()(argument_type0&& div_lm, argument_type1&& self_nlm) const
  {
    ;
    ;
    return pythonic::types::make_tuple(pythonic::numpy::functor::empty{}(self_nlm, pythonic::__builtin__::functor::complex{}));
  }
  typename __transonic__::type::result_type __transonic__::operator()() const
  {
    {
      static typename __transonic__::type::result_type tmp_global = pythonic::types::make_tuple(pythonic::types::str("0.4.1"));
      return tmp_global;
    }
  }
  typename __code_new_method__OperatorsSphereHarmo2D__vsh_from_divrotsh::type::result_type __code_new_method__OperatorsSphereHarmo2D__vsh_from_divrotsh::operator()() const
  {
    {
      static typename __code_new_method__OperatorsSphereHarmo2D__vsh_from_divrotsh::type::result_type tmp_global = pythonic::types::str("\n"
"\n"
"def new_method(self, div_lm, rot_lm, uD_lm=None, uR_lm=None):\n"
"    return backend_func(self.inv_K2_r, self.nlm, div_lm, rot_lm, uD_lm, uR_lm)\n"
"\n"
"");
      return tmp_global;
    }
  }
  typename __code_new_method__OperatorsSphereHarmo2D__divrotsh_from_vsh::type::result_type __code_new_method__OperatorsSphereHarmo2D__divrotsh_from_vsh::operator()() const
  {
    {
      static typename __code_new_method__OperatorsSphereHarmo2D__divrotsh_from_vsh::type::result_type tmp_global = pythonic::types::str("\n"
"\n"
"def new_method(self, uD_lm, uR_lm, div_lm=None, rot_lm=None):\n"
"    return backend_func(self.K2_r, self.nlm, uD_lm, uR_lm, div_lm, rot_lm)\n"
"\n"
"");
      return tmp_global;
    }
  }
  typename __code_new_method__OperatorsSphereHarmo2D__invlaplacian_sh::type::result_type __code_new_method__OperatorsSphereHarmo2D__invlaplacian_sh::operator()() const
  {
    {
      static typename __code_new_method__OperatorsSphereHarmo2D__invlaplacian_sh::type::result_type tmp_global = pythonic::types::str("\n"
"\n"
"def new_method(self, a_lm, negative=False):\n"
"    return backend_func(self.inv_K2_not0, a_lm, negative)\n"
"\n"
"");
      return tmp_global;
    }
  }
  template <typename argument_type0 , typename argument_type1 , typename argument_type2 >
  typename __for_method__OperatorsSphereHarmo2D__invlaplacian_sh::type<argument_type0, argument_type1, argument_type2>::result_type __for_method__OperatorsSphereHarmo2D__invlaplacian_sh::operator()(argument_type0&& self_inv_K2_not0, argument_type1&& a_lm, argument_type2 negative) const
  {
    if (negative)
    {
      return (pythonic::operator_::mul(self_inv_K2_not0, a_lm));
    }
    else
    {
      return (pythonic::operator_::mul((-self_inv_K2_not0), a_lm));
    }
  }
  typename __code_new_method__OperatorsSphereHarmo2D__laplacian_sh::type::result_type __code_new_method__OperatorsSphereHarmo2D__laplacian_sh::operator()() const
  {
    {
      static typename __code_new_method__OperatorsSphereHarmo2D__laplacian_sh::type::result_type tmp_global = pythonic::types::str("\n"
"\n"
"def new_method(self, a_lm, negative=False):\n"
"    return backend_func(self.K2, a_lm, negative)\n"
"\n"
"");
      return tmp_global;
    }
  }
  template <typename argument_type0 , typename argument_type1 , typename argument_type2 >
  typename __for_method__OperatorsSphereHarmo2D__laplacian_sh::type<argument_type0, argument_type1, argument_type2>::result_type __for_method__OperatorsSphereHarmo2D__laplacian_sh::operator()(argument_type0&& self_K2, argument_type1&& a_lm, argument_type2 negative) const
  {
    if (negative)
    {
      return (pythonic::operator_::mul(self_K2, a_lm));
    }
    else
    {
      return (pythonic::operator_::mul((-self_K2), a_lm));
    }
  }
  template <typename argument_type0 , typename argument_type1 , typename argument_type2 , typename argument_type3 , typename argument_type4 , typename argument_type5 >
  typename __for_method__OperatorsSphereHarmo2D__vsh_from_divrotsh::type<argument_type0, argument_type1, argument_type2, argument_type3, argument_type4, argument_type5>::result_type __for_method__OperatorsSphereHarmo2D__vsh_from_divrotsh::operator()(argument_type0&& self_inv_K2_r, argument_type1&& self_nlm, argument_type2&& div_lm, argument_type3&& rot_lm, argument_type4 uD_lm, argument_type5 uR_lm) const
  {
    typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::__builtin__::pythran::functor::static_if{})>::type>::type __type0;
    typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::__builtin__::pythran::functor::is_none{})>::type>::type __type1;
    typedef typename pythonic::assignable<typename std::remove_cv<typename std::remove_reference<argument_type4>::type>::type>::type __type2;
    typedef decltype(std::declval<__type1>()(std::declval<__type2>())) __type3;
    typedef $isstatic4 __type4;
    typedef $isstatic5 __type5;
    typedef decltype(std::declval<__type0>()(std::declval<__type3>(), std::declval<__type4>(), std::declval<__type5>())) __type6;
    typedef typename std::remove_cv<typename std::remove_reference<argument_type1>::type>::type __type7;
    typedef typename pythonic::assignable<decltype(std::declval<__type6>()(std::declval<__type7>(), std::declval<__type2>()))>::type __type8;
    typedef typename pythonic::assignable<typename std::tuple_element<0,typename std::remove_reference<__type8>::type>::type>::type __type9;
    typedef typename std::remove_cv<typename std::remove_reference<argument_type2>::type>::type __type10;
    typedef decltype((-std::declval<__type10>())) __type11;
    typedef typename std::remove_cv<typename std::remove_reference<argument_type0>::type>::type __type12;
    typedef decltype((pythonic::operator_::mul(std::declval<__type11>(), std::declval<__type12>()))) __type13;
    typedef typename pythonic::assignable<typename std::remove_cv<typename std::remove_reference<argument_type5>::type>::type>::type __type14;
    typedef decltype(std::declval<__type1>()(std::declval<__type14>())) __type15;
    typedef $isstatic6 __type16;
    typedef $isstatic7 __type17;
    typedef decltype(std::declval<__type0>()(std::declval<__type15>(), std::declval<__type16>(), std::declval<__type17>())) __type18;
    typedef typename pythonic::assignable<decltype(std::declval<__type18>()(std::declval<__type7>(), std::declval<__type14>()))>::type __type19;
    typedef typename pythonic::assignable<typename std::tuple_element<0,typename std::remove_reference<__type19>::type>::type>::type __type20;
    typedef typename std::remove_cv<typename std::remove_reference<argument_type3>::type>::type __type21;
    typedef decltype((pythonic::operator_::mul(std::declval<__type21>(), std::declval<__type12>()))) __type22;
    typename pythonic::assignable<decltype(uR_lm)>::type uR_lm_ = uR_lm;
    typename pythonic::assignable<decltype(uD_lm)>::type uD_lm_ = uD_lm;
    typename pythonic::assignable<decltype(pythonic::__builtin__::pythran::functor::static_if{}(pythonic::__builtin__::pythran::functor::is_none{}(uD_lm_), $isstatic4(), $isstatic5())(self_nlm, uD_lm_))>::type __tuple0 = pythonic::__builtin__::pythran::functor::static_if{}(pythonic::__builtin__::pythran::functor::is_none{}(uD_lm_), $isstatic4(), $isstatic5())(self_nlm, uD_lm_);
    typename pythonic::assignable<typename __combined<__type9,__type13>::type>::type uD_lm__ = std::get<0>(__tuple0);
    typename pythonic::assignable<decltype(pythonic::__builtin__::pythran::functor::static_if{}(pythonic::__builtin__::pythran::functor::is_none{}(uR_lm_), $isstatic6(), $isstatic7())(self_nlm, uR_lm_))>::type __tuple1 = pythonic::__builtin__::pythran::functor::static_if{}(pythonic::__builtin__::pythran::functor::is_none{}(uR_lm_), $isstatic6(), $isstatic7())(self_nlm, uR_lm_);
    typename pythonic::assignable<typename __combined<__type20,__type22>::type>::type uR_lm__ = std::get<0>(__tuple1);
    uD_lm__[pythonic::types::contiguous_slice(pythonic::__builtin__::None,pythonic::__builtin__::None)] = (pythonic::operator_::mul((-div_lm), self_inv_K2_r));
    uR_lm__[pythonic::types::contiguous_slice(pythonic::__builtin__::None,pythonic::__builtin__::None)] = (pythonic::operator_::mul(rot_lm, self_inv_K2_r));
    return pythonic::types::make_tuple(uD_lm__, uR_lm__);
  }
  template <typename argument_type0 , typename argument_type1 , typename argument_type2 , typename argument_type3 , typename argument_type4 , typename argument_type5 >
  typename __for_method__OperatorsSphereHarmo2D__divrotsh_from_vsh::type<argument_type0, argument_type1, argument_type2, argument_type3, argument_type4, argument_type5>::result_type __for_method__OperatorsSphereHarmo2D__divrotsh_from_vsh::operator()(argument_type0&& self_K2_r, argument_type1&& self_nlm, argument_type2&& uD_lm, argument_type3&& uR_lm, argument_type4 div_lm, argument_type5 rot_lm) const
  {
    typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::__builtin__::pythran::functor::static_if{})>::type>::type __type0;
    typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::__builtin__::pythran::functor::is_none{})>::type>::type __type1;
    typedef typename pythonic::assignable<typename std::remove_cv<typename std::remove_reference<argument_type4>::type>::type>::type __type2;
    typedef decltype(std::declval<__type1>()(std::declval<__type2>())) __type3;
    typedef $isstatic0 __type4;
    typedef $isstatic1 __type5;
    typedef decltype(std::declval<__type0>()(std::declval<__type3>(), std::declval<__type4>(), std::declval<__type5>())) __type6;
    typedef typename std::remove_cv<typename std::remove_reference<argument_type1>::type>::type __type7;
    typedef typename pythonic::assignable<decltype(std::declval<__type6>()(std::declval<__type2>(), std::declval<__type7>()))>::type __type8;
    typedef typename pythonic::assignable<typename std::tuple_element<0,typename std::remove_reference<__type8>::type>::type>::type __type9;
    typedef typename std::remove_cv<typename std::remove_reference<argument_type0>::type>::type __type10;
    typedef decltype((-std::declval<__type10>())) __type11;
    typedef typename std::remove_cv<typename std::remove_reference<argument_type2>::type>::type __type12;
    typedef decltype((pythonic::operator_::mul(std::declval<__type11>(), std::declval<__type12>()))) __type13;
    typedef typename pythonic::assignable<typename std::remove_cv<typename std::remove_reference<argument_type5>::type>::type>::type __type14;
    typedef decltype(std::declval<__type1>()(std::declval<__type14>())) __type15;
    typedef $isstatic2 __type16;
    typedef $isstatic3 __type17;
    typedef decltype(std::declval<__type0>()(std::declval<__type15>(), std::declval<__type16>(), std::declval<__type17>())) __type18;
    typedef typename pythonic::assignable<decltype(std::declval<__type18>()(std::declval<__type14>(), std::declval<__type7>()))>::type __type19;
    typedef typename pythonic::assignable<typename std::tuple_element<0,typename std::remove_reference<__type19>::type>::type>::type __type20;
    typedef typename std::remove_cv<typename std::remove_reference<argument_type3>::type>::type __type21;
    typedef decltype((pythonic::operator_::mul(std::declval<__type10>(), std::declval<__type21>()))) __type22;
    typename pythonic::assignable<decltype(rot_lm)>::type rot_lm_ = rot_lm;
    typename pythonic::assignable<decltype(div_lm)>::type div_lm_ = div_lm;
    typename pythonic::assignable<decltype(pythonic::__builtin__::pythran::functor::static_if{}(pythonic::__builtin__::pythran::functor::is_none{}(div_lm_), $isstatic0(), $isstatic1())(div_lm_, self_nlm))>::type __tuple0 = pythonic::__builtin__::pythran::functor::static_if{}(pythonic::__builtin__::pythran::functor::is_none{}(div_lm_), $isstatic0(), $isstatic1())(div_lm_, self_nlm);
    typename pythonic::assignable<typename __combined<__type9,__type13>::type>::type div_lm__ = std::get<0>(__tuple0);
    typename pythonic::assignable<decltype(pythonic::__builtin__::pythran::functor::static_if{}(pythonic::__builtin__::pythran::functor::is_none{}(rot_lm_), $isstatic2(), $isstatic3())(rot_lm_, self_nlm))>::type __tuple1 = pythonic::__builtin__::pythran::functor::static_if{}(pythonic::__builtin__::pythran::functor::is_none{}(rot_lm_), $isstatic2(), $isstatic3())(rot_lm_, self_nlm);
    typename pythonic::assignable<typename __combined<__type20,__type22>::type>::type rot_lm__ = std::get<0>(__tuple1);
    div_lm__[pythonic::types::contiguous_slice(pythonic::__builtin__::None,pythonic::__builtin__::None)] = (pythonic::operator_::mul((-self_K2_r), uD_lm));
    rot_lm__[pythonic::types::contiguous_slice(pythonic::__builtin__::None,pythonic::__builtin__::None)] = (pythonic::operator_::mul(self_K2_r, uR_lm));
    return pythonic::types::make_tuple(div_lm__, rot_lm__);
  }
}
#include <pythonic/python/exception_handler.hpp>
#ifdef ENABLE_PYTHON_MODULE
static PyObject* __transonic__ = to_python(__pythran_operators::__transonic__()());
static PyObject* __code_new_method__OperatorsSphereHarmo2D__vsh_from_divrotsh = to_python(__pythran_operators::__code_new_method__OperatorsSphereHarmo2D__vsh_from_divrotsh()());
typename __pythran_operators::__for_method__OperatorsSphereHarmo2D__vsh_from_divrotsh::type<pythonic::types::ndarray<double,pythonic::types::pshape<long>>, long, pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long>>, pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long>>, pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long>>, pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long>>>::result_type __for_method__OperatorsSphereHarmo2D__vsh_from_divrotsh0(pythonic::types::ndarray<double,pythonic::types::pshape<long>>&& self_inv_K2_r, long&& self_nlm, pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long>>&& div_lm, pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long>>&& rot_lm, pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long>>&& uD_lm, pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long>>&& uR_lm) 
{
  
                            PyThreadState *_save = PyEval_SaveThread();
                            try {
                                auto res = __pythran_operators::__for_method__OperatorsSphereHarmo2D__vsh_from_divrotsh()(self_inv_K2_r, self_nlm, div_lm, rot_lm, uD_lm, uR_lm);
                                PyEval_RestoreThread(_save);
                                return res;
                            }
                            catch(...) {
                                PyEval_RestoreThread(_save);
                                throw;
                            }
                            ;
}
typename __pythran_operators::__for_method__OperatorsSphereHarmo2D__vsh_from_divrotsh::type<pythonic::types::ndarray<double,pythonic::types::pshape<long>>, long, pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long>>, pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long>>, pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long>>, pythonic::types::none_type>::result_type __for_method__OperatorsSphereHarmo2D__vsh_from_divrotsh1(pythonic::types::ndarray<double,pythonic::types::pshape<long>>&& self_inv_K2_r, long&& self_nlm, pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long>>&& div_lm, pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long>>&& rot_lm, pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long>>&& uD_lm, pythonic::types::none_type&& uR_lm) 
{
  
                            PyThreadState *_save = PyEval_SaveThread();
                            try {
                                auto res = __pythran_operators::__for_method__OperatorsSphereHarmo2D__vsh_from_divrotsh()(self_inv_K2_r, self_nlm, div_lm, rot_lm, uD_lm, uR_lm);
                                PyEval_RestoreThread(_save);
                                return res;
                            }
                            catch(...) {
                                PyEval_RestoreThread(_save);
                                throw;
                            }
                            ;
}
typename __pythran_operators::__for_method__OperatorsSphereHarmo2D__vsh_from_divrotsh::type<pythonic::types::ndarray<double,pythonic::types::pshape<long>>, long, pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long>>, pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long>>, pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long>>>::result_type __for_method__OperatorsSphereHarmo2D__vsh_from_divrotsh2(pythonic::types::ndarray<double,pythonic::types::pshape<long>>&& self_inv_K2_r, long&& self_nlm, pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long>>&& div_lm, pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long>>&& rot_lm, pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long>>&& uD_lm) 
{
  
                            PyThreadState *_save = PyEval_SaveThread();
                            try {
                                auto res = __pythran_operators::__for_method__OperatorsSphereHarmo2D__vsh_from_divrotsh()(self_inv_K2_r, self_nlm, div_lm, rot_lm, uD_lm);
                                PyEval_RestoreThread(_save);
                                return res;
                            }
                            catch(...) {
                                PyEval_RestoreThread(_save);
                                throw;
                            }
                            ;
}
typename __pythran_operators::__for_method__OperatorsSphereHarmo2D__vsh_from_divrotsh::type<pythonic::types::ndarray<double,pythonic::types::pshape<long>>, long, pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long>>, pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long>>, pythonic::types::none_type, pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long>>>::result_type __for_method__OperatorsSphereHarmo2D__vsh_from_divrotsh3(pythonic::types::ndarray<double,pythonic::types::pshape<long>>&& self_inv_K2_r, long&& self_nlm, pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long>>&& div_lm, pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long>>&& rot_lm, pythonic::types::none_type&& uD_lm, pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long>>&& uR_lm) 
{
  
                            PyThreadState *_save = PyEval_SaveThread();
                            try {
                                auto res = __pythran_operators::__for_method__OperatorsSphereHarmo2D__vsh_from_divrotsh()(self_inv_K2_r, self_nlm, div_lm, rot_lm, uD_lm, uR_lm);
                                PyEval_RestoreThread(_save);
                                return res;
                            }
                            catch(...) {
                                PyEval_RestoreThread(_save);
                                throw;
                            }
                            ;
}
typename __pythran_operators::__for_method__OperatorsSphereHarmo2D__vsh_from_divrotsh::type<pythonic::types::ndarray<double,pythonic::types::pshape<long>>, long, pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long>>, pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long>>, pythonic::types::none_type, pythonic::types::none_type>::result_type __for_method__OperatorsSphereHarmo2D__vsh_from_divrotsh4(pythonic::types::ndarray<double,pythonic::types::pshape<long>>&& self_inv_K2_r, long&& self_nlm, pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long>>&& div_lm, pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long>>&& rot_lm, pythonic::types::none_type&& uD_lm, pythonic::types::none_type&& uR_lm) 
{
  
                            PyThreadState *_save = PyEval_SaveThread();
                            try {
                                auto res = __pythran_operators::__for_method__OperatorsSphereHarmo2D__vsh_from_divrotsh()(self_inv_K2_r, self_nlm, div_lm, rot_lm, uD_lm, uR_lm);
                                PyEval_RestoreThread(_save);
                                return res;
                            }
                            catch(...) {
                                PyEval_RestoreThread(_save);
                                throw;
                            }
                            ;
}
typename __pythran_operators::__for_method__OperatorsSphereHarmo2D__vsh_from_divrotsh::type<pythonic::types::ndarray<double,pythonic::types::pshape<long>>, long, pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long>>, pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long>>, pythonic::types::none_type>::result_type __for_method__OperatorsSphereHarmo2D__vsh_from_divrotsh5(pythonic::types::ndarray<double,pythonic::types::pshape<long>>&& self_inv_K2_r, long&& self_nlm, pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long>>&& div_lm, pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long>>&& rot_lm, pythonic::types::none_type&& uD_lm) 
{
  
                            PyThreadState *_save = PyEval_SaveThread();
                            try {
                                auto res = __pythran_operators::__for_method__OperatorsSphereHarmo2D__vsh_from_divrotsh()(self_inv_K2_r, self_nlm, div_lm, rot_lm, uD_lm);
                                PyEval_RestoreThread(_save);
                                return res;
                            }
                            catch(...) {
                                PyEval_RestoreThread(_save);
                                throw;
                            }
                            ;
}
typename __pythran_operators::__for_method__OperatorsSphereHarmo2D__vsh_from_divrotsh::type<pythonic::types::ndarray<double,pythonic::types::pshape<long>>, long, pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long>>, pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long>>>::result_type __for_method__OperatorsSphereHarmo2D__vsh_from_divrotsh6(pythonic::types::ndarray<double,pythonic::types::pshape<long>>&& self_inv_K2_r, long&& self_nlm, pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long>>&& div_lm, pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long>>&& rot_lm) 
{
  
                            PyThreadState *_save = PyEval_SaveThread();
                            try {
                                auto res = __pythran_operators::__for_method__OperatorsSphereHarmo2D__vsh_from_divrotsh()(self_inv_K2_r, self_nlm, div_lm, rot_lm);
                                PyEval_RestoreThread(_save);
                                return res;
                            }
                            catch(...) {
                                PyEval_RestoreThread(_save);
                                throw;
                            }
                            ;
}
static PyObject* __code_new_method__OperatorsSphereHarmo2D__divrotsh_from_vsh = to_python(__pythran_operators::__code_new_method__OperatorsSphereHarmo2D__divrotsh_from_vsh()());
typename __pythran_operators::__for_method__OperatorsSphereHarmo2D__divrotsh_from_vsh::type<pythonic::types::ndarray<double,pythonic::types::pshape<long>>, long, pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long>>, pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long>>, pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long>>, pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long>>>::result_type __for_method__OperatorsSphereHarmo2D__divrotsh_from_vsh0(pythonic::types::ndarray<double,pythonic::types::pshape<long>>&& self_K2_r, long&& self_nlm, pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long>>&& uD_lm, pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long>>&& uR_lm, pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long>>&& div_lm, pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long>>&& rot_lm) 
{
  
                            PyThreadState *_save = PyEval_SaveThread();
                            try {
                                auto res = __pythran_operators::__for_method__OperatorsSphereHarmo2D__divrotsh_from_vsh()(self_K2_r, self_nlm, uD_lm, uR_lm, div_lm, rot_lm);
                                PyEval_RestoreThread(_save);
                                return res;
                            }
                            catch(...) {
                                PyEval_RestoreThread(_save);
                                throw;
                            }
                            ;
}
typename __pythran_operators::__for_method__OperatorsSphereHarmo2D__divrotsh_from_vsh::type<pythonic::types::ndarray<double,pythonic::types::pshape<long>>, long, pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long>>, pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long>>, pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long>>, pythonic::types::none_type>::result_type __for_method__OperatorsSphereHarmo2D__divrotsh_from_vsh1(pythonic::types::ndarray<double,pythonic::types::pshape<long>>&& self_K2_r, long&& self_nlm, pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long>>&& uD_lm, pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long>>&& uR_lm, pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long>>&& div_lm, pythonic::types::none_type&& rot_lm) 
{
  
                            PyThreadState *_save = PyEval_SaveThread();
                            try {
                                auto res = __pythran_operators::__for_method__OperatorsSphereHarmo2D__divrotsh_from_vsh()(self_K2_r, self_nlm, uD_lm, uR_lm, div_lm, rot_lm);
                                PyEval_RestoreThread(_save);
                                return res;
                            }
                            catch(...) {
                                PyEval_RestoreThread(_save);
                                throw;
                            }
                            ;
}
typename __pythran_operators::__for_method__OperatorsSphereHarmo2D__divrotsh_from_vsh::type<pythonic::types::ndarray<double,pythonic::types::pshape<long>>, long, pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long>>, pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long>>, pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long>>>::result_type __for_method__OperatorsSphereHarmo2D__divrotsh_from_vsh2(pythonic::types::ndarray<double,pythonic::types::pshape<long>>&& self_K2_r, long&& self_nlm, pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long>>&& uD_lm, pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long>>&& uR_lm, pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long>>&& div_lm) 
{
  
                            PyThreadState *_save = PyEval_SaveThread();
                            try {
                                auto res = __pythran_operators::__for_method__OperatorsSphereHarmo2D__divrotsh_from_vsh()(self_K2_r, self_nlm, uD_lm, uR_lm, div_lm);
                                PyEval_RestoreThread(_save);
                                return res;
                            }
                            catch(...) {
                                PyEval_RestoreThread(_save);
                                throw;
                            }
                            ;
}
typename __pythran_operators::__for_method__OperatorsSphereHarmo2D__divrotsh_from_vsh::type<pythonic::types::ndarray<double,pythonic::types::pshape<long>>, long, pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long>>, pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long>>, pythonic::types::none_type, pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long>>>::result_type __for_method__OperatorsSphereHarmo2D__divrotsh_from_vsh3(pythonic::types::ndarray<double,pythonic::types::pshape<long>>&& self_K2_r, long&& self_nlm, pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long>>&& uD_lm, pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long>>&& uR_lm, pythonic::types::none_type&& div_lm, pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long>>&& rot_lm) 
{
  
                            PyThreadState *_save = PyEval_SaveThread();
                            try {
                                auto res = __pythran_operators::__for_method__OperatorsSphereHarmo2D__divrotsh_from_vsh()(self_K2_r, self_nlm, uD_lm, uR_lm, div_lm, rot_lm);
                                PyEval_RestoreThread(_save);
                                return res;
                            }
                            catch(...) {
                                PyEval_RestoreThread(_save);
                                throw;
                            }
                            ;
}
typename __pythran_operators::__for_method__OperatorsSphereHarmo2D__divrotsh_from_vsh::type<pythonic::types::ndarray<double,pythonic::types::pshape<long>>, long, pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long>>, pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long>>, pythonic::types::none_type, pythonic::types::none_type>::result_type __for_method__OperatorsSphereHarmo2D__divrotsh_from_vsh4(pythonic::types::ndarray<double,pythonic::types::pshape<long>>&& self_K2_r, long&& self_nlm, pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long>>&& uD_lm, pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long>>&& uR_lm, pythonic::types::none_type&& div_lm, pythonic::types::none_type&& rot_lm) 
{
  
                            PyThreadState *_save = PyEval_SaveThread();
                            try {
                                auto res = __pythran_operators::__for_method__OperatorsSphereHarmo2D__divrotsh_from_vsh()(self_K2_r, self_nlm, uD_lm, uR_lm, div_lm, rot_lm);
                                PyEval_RestoreThread(_save);
                                return res;
                            }
                            catch(...) {
                                PyEval_RestoreThread(_save);
                                throw;
                            }
                            ;
}
typename __pythran_operators::__for_method__OperatorsSphereHarmo2D__divrotsh_from_vsh::type<pythonic::types::ndarray<double,pythonic::types::pshape<long>>, long, pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long>>, pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long>>, pythonic::types::none_type>::result_type __for_method__OperatorsSphereHarmo2D__divrotsh_from_vsh5(pythonic::types::ndarray<double,pythonic::types::pshape<long>>&& self_K2_r, long&& self_nlm, pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long>>&& uD_lm, pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long>>&& uR_lm, pythonic::types::none_type&& div_lm) 
{
  
                            PyThreadState *_save = PyEval_SaveThread();
                            try {
                                auto res = __pythran_operators::__for_method__OperatorsSphereHarmo2D__divrotsh_from_vsh()(self_K2_r, self_nlm, uD_lm, uR_lm, div_lm);
                                PyEval_RestoreThread(_save);
                                return res;
                            }
                            catch(...) {
                                PyEval_RestoreThread(_save);
                                throw;
                            }
                            ;
}
typename __pythran_operators::__for_method__OperatorsSphereHarmo2D__divrotsh_from_vsh::type<pythonic::types::ndarray<double,pythonic::types::pshape<long>>, long, pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long>>, pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long>>>::result_type __for_method__OperatorsSphereHarmo2D__divrotsh_from_vsh6(pythonic::types::ndarray<double,pythonic::types::pshape<long>>&& self_K2_r, long&& self_nlm, pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long>>&& uD_lm, pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long>>&& uR_lm) 
{
  
                            PyThreadState *_save = PyEval_SaveThread();
                            try {
                                auto res = __pythran_operators::__for_method__OperatorsSphereHarmo2D__divrotsh_from_vsh()(self_K2_r, self_nlm, uD_lm, uR_lm);
                                PyEval_RestoreThread(_save);
                                return res;
                            }
                            catch(...) {
                                PyEval_RestoreThread(_save);
                                throw;
                            }
                            ;
}
static PyObject* __code_new_method__OperatorsSphereHarmo2D__invlaplacian_sh = to_python(__pythran_operators::__code_new_method__OperatorsSphereHarmo2D__invlaplacian_sh()());
typename __pythran_operators::__for_method__OperatorsSphereHarmo2D__invlaplacian_sh::type<pythonic::types::ndarray<double,pythonic::types::pshape<long>>, pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long>>, bool>::result_type __for_method__OperatorsSphereHarmo2D__invlaplacian_sh0(pythonic::types::ndarray<double,pythonic::types::pshape<long>>&& self_inv_K2_not0, pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long>>&& a_lm, bool&& negative) 
{
  
                            PyThreadState *_save = PyEval_SaveThread();
                            try {
                                auto res = __pythran_operators::__for_method__OperatorsSphereHarmo2D__invlaplacian_sh()(self_inv_K2_not0, a_lm, negative);
                                PyEval_RestoreThread(_save);
                                return res;
                            }
                            catch(...) {
                                PyEval_RestoreThread(_save);
                                throw;
                            }
                            ;
}
typename __pythran_operators::__for_method__OperatorsSphereHarmo2D__invlaplacian_sh::type<pythonic::types::ndarray<double,pythonic::types::pshape<long>>, pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long>>>::result_type __for_method__OperatorsSphereHarmo2D__invlaplacian_sh1(pythonic::types::ndarray<double,pythonic::types::pshape<long>>&& self_inv_K2_not0, pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long>>&& a_lm) 
{
  
                            PyThreadState *_save = PyEval_SaveThread();
                            try {
                                auto res = __pythran_operators::__for_method__OperatorsSphereHarmo2D__invlaplacian_sh()(self_inv_K2_not0, a_lm);
                                PyEval_RestoreThread(_save);
                                return res;
                            }
                            catch(...) {
                                PyEval_RestoreThread(_save);
                                throw;
                            }
                            ;
}
static PyObject* __code_new_method__OperatorsSphereHarmo2D__laplacian_sh = to_python(__pythran_operators::__code_new_method__OperatorsSphereHarmo2D__laplacian_sh()());
typename __pythran_operators::__for_method__OperatorsSphereHarmo2D__laplacian_sh::type<pythonic::types::ndarray<double,pythonic::types::pshape<long>>, pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long>>, bool>::result_type __for_method__OperatorsSphereHarmo2D__laplacian_sh0(pythonic::types::ndarray<double,pythonic::types::pshape<long>>&& self_K2, pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long>>&& a_lm, bool&& negative) 
{
  
                            PyThreadState *_save = PyEval_SaveThread();
                            try {
                                auto res = __pythran_operators::__for_method__OperatorsSphereHarmo2D__laplacian_sh()(self_K2, a_lm, negative);
                                PyEval_RestoreThread(_save);
                                return res;
                            }
                            catch(...) {
                                PyEval_RestoreThread(_save);
                                throw;
                            }
                            ;
}
typename __pythran_operators::__for_method__OperatorsSphereHarmo2D__laplacian_sh::type<pythonic::types::ndarray<double,pythonic::types::pshape<long>>, pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long>>>::result_type __for_method__OperatorsSphereHarmo2D__laplacian_sh1(pythonic::types::ndarray<double,pythonic::types::pshape<long>>&& self_K2, pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long>>&& a_lm) 
{
  
                            PyThreadState *_save = PyEval_SaveThread();
                            try {
                                auto res = __pythran_operators::__for_method__OperatorsSphereHarmo2D__laplacian_sh()(self_K2, a_lm);
                                PyEval_RestoreThread(_save);
                                return res;
                            }
                            catch(...) {
                                PyEval_RestoreThread(_save);
                                throw;
                            }
                            ;
}

static PyObject *
__pythran_wrap___for_method__OperatorsSphereHarmo2D__vsh_from_divrotsh0(PyObject *self, PyObject *args, PyObject *kw)
{
    PyObject* args_obj[6+1];
    char const* keywords[] = {"self_inv_K2_r","self_nlm","div_lm","rot_lm","uD_lm","uR_lm", nullptr};
    if(! PyArg_ParseTupleAndKeywords(args, kw, "OOOOOO",
                                     (char**)keywords, &args_obj[0], &args_obj[1], &args_obj[2], &args_obj[3], &args_obj[4], &args_obj[5]))
        return nullptr;
    if(is_convertible<pythonic::types::ndarray<double,pythonic::types::pshape<long>>>(args_obj[0]) && is_convertible<long>(args_obj[1]) && is_convertible<pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long>>>(args_obj[2]) && is_convertible<pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long>>>(args_obj[3]) && is_convertible<pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long>>>(args_obj[4]) && is_convertible<pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long>>>(args_obj[5]))
        return to_python(__for_method__OperatorsSphereHarmo2D__vsh_from_divrotsh0(from_python<pythonic::types::ndarray<double,pythonic::types::pshape<long>>>(args_obj[0]), from_python<long>(args_obj[1]), from_python<pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long>>>(args_obj[2]), from_python<pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long>>>(args_obj[3]), from_python<pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long>>>(args_obj[4]), from_python<pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long>>>(args_obj[5])));
    else {
        return nullptr;
    }
}

static PyObject *
__pythran_wrap___for_method__OperatorsSphereHarmo2D__vsh_from_divrotsh1(PyObject *self, PyObject *args, PyObject *kw)
{
    PyObject* args_obj[6+1];
    char const* keywords[] = {"self_inv_K2_r","self_nlm","div_lm","rot_lm","uD_lm","uR_lm", nullptr};
    if(! PyArg_ParseTupleAndKeywords(args, kw, "OOOOOO",
                                     (char**)keywords, &args_obj[0], &args_obj[1], &args_obj[2], &args_obj[3], &args_obj[4], &args_obj[5]))
        return nullptr;
    if(is_convertible<pythonic::types::ndarray<double,pythonic::types::pshape<long>>>(args_obj[0]) && is_convertible<long>(args_obj[1]) && is_convertible<pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long>>>(args_obj[2]) && is_convertible<pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long>>>(args_obj[3]) && is_convertible<pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long>>>(args_obj[4]) && is_convertible<pythonic::types::none_type>(args_obj[5]))
        return to_python(__for_method__OperatorsSphereHarmo2D__vsh_from_divrotsh1(from_python<pythonic::types::ndarray<double,pythonic::types::pshape<long>>>(args_obj[0]), from_python<long>(args_obj[1]), from_python<pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long>>>(args_obj[2]), from_python<pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long>>>(args_obj[3]), from_python<pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long>>>(args_obj[4]), from_python<pythonic::types::none_type>(args_obj[5])));
    else {
        return nullptr;
    }
}

static PyObject *
__pythran_wrap___for_method__OperatorsSphereHarmo2D__vsh_from_divrotsh2(PyObject *self, PyObject *args, PyObject *kw)
{
    PyObject* args_obj[5+1];
    char const* keywords[] = {"self_inv_K2_r","self_nlm","div_lm","rot_lm","uD_lm", nullptr};
    if(! PyArg_ParseTupleAndKeywords(args, kw, "OOOOO",
                                     (char**)keywords, &args_obj[0], &args_obj[1], &args_obj[2], &args_obj[3], &args_obj[4]))
        return nullptr;
    if(is_convertible<pythonic::types::ndarray<double,pythonic::types::pshape<long>>>(args_obj[0]) && is_convertible<long>(args_obj[1]) && is_convertible<pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long>>>(args_obj[2]) && is_convertible<pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long>>>(args_obj[3]) && is_convertible<pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long>>>(args_obj[4]))
        return to_python(__for_method__OperatorsSphereHarmo2D__vsh_from_divrotsh2(from_python<pythonic::types::ndarray<double,pythonic::types::pshape<long>>>(args_obj[0]), from_python<long>(args_obj[1]), from_python<pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long>>>(args_obj[2]), from_python<pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long>>>(args_obj[3]), from_python<pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long>>>(args_obj[4])));
    else {
        return nullptr;
    }
}

static PyObject *
__pythran_wrap___for_method__OperatorsSphereHarmo2D__vsh_from_divrotsh3(PyObject *self, PyObject *args, PyObject *kw)
{
    PyObject* args_obj[6+1];
    char const* keywords[] = {"self_inv_K2_r","self_nlm","div_lm","rot_lm","uD_lm","uR_lm", nullptr};
    if(! PyArg_ParseTupleAndKeywords(args, kw, "OOOOOO",
                                     (char**)keywords, &args_obj[0], &args_obj[1], &args_obj[2], &args_obj[3], &args_obj[4], &args_obj[5]))
        return nullptr;
    if(is_convertible<pythonic::types::ndarray<double,pythonic::types::pshape<long>>>(args_obj[0]) && is_convertible<long>(args_obj[1]) && is_convertible<pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long>>>(args_obj[2]) && is_convertible<pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long>>>(args_obj[3]) && is_convertible<pythonic::types::none_type>(args_obj[4]) && is_convertible<pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long>>>(args_obj[5]))
        return to_python(__for_method__OperatorsSphereHarmo2D__vsh_from_divrotsh3(from_python<pythonic::types::ndarray<double,pythonic::types::pshape<long>>>(args_obj[0]), from_python<long>(args_obj[1]), from_python<pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long>>>(args_obj[2]), from_python<pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long>>>(args_obj[3]), from_python<pythonic::types::none_type>(args_obj[4]), from_python<pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long>>>(args_obj[5])));
    else {
        return nullptr;
    }
}

static PyObject *
__pythran_wrap___for_method__OperatorsSphereHarmo2D__vsh_from_divrotsh4(PyObject *self, PyObject *args, PyObject *kw)
{
    PyObject* args_obj[6+1];
    char const* keywords[] = {"self_inv_K2_r","self_nlm","div_lm","rot_lm","uD_lm","uR_lm", nullptr};
    if(! PyArg_ParseTupleAndKeywords(args, kw, "OOOOOO",
                                     (char**)keywords, &args_obj[0], &args_obj[1], &args_obj[2], &args_obj[3], &args_obj[4], &args_obj[5]))
        return nullptr;
    if(is_convertible<pythonic::types::ndarray<double,pythonic::types::pshape<long>>>(args_obj[0]) && is_convertible<long>(args_obj[1]) && is_convertible<pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long>>>(args_obj[2]) && is_convertible<pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long>>>(args_obj[3]) && is_convertible<pythonic::types::none_type>(args_obj[4]) && is_convertible<pythonic::types::none_type>(args_obj[5]))
        return to_python(__for_method__OperatorsSphereHarmo2D__vsh_from_divrotsh4(from_python<pythonic::types::ndarray<double,pythonic::types::pshape<long>>>(args_obj[0]), from_python<long>(args_obj[1]), from_python<pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long>>>(args_obj[2]), from_python<pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long>>>(args_obj[3]), from_python<pythonic::types::none_type>(args_obj[4]), from_python<pythonic::types::none_type>(args_obj[5])));
    else {
        return nullptr;
    }
}

static PyObject *
__pythran_wrap___for_method__OperatorsSphereHarmo2D__vsh_from_divrotsh5(PyObject *self, PyObject *args, PyObject *kw)
{
    PyObject* args_obj[5+1];
    char const* keywords[] = {"self_inv_K2_r","self_nlm","div_lm","rot_lm","uD_lm", nullptr};
    if(! PyArg_ParseTupleAndKeywords(args, kw, "OOOOO",
                                     (char**)keywords, &args_obj[0], &args_obj[1], &args_obj[2], &args_obj[3], &args_obj[4]))
        return nullptr;
    if(is_convertible<pythonic::types::ndarray<double,pythonic::types::pshape<long>>>(args_obj[0]) && is_convertible<long>(args_obj[1]) && is_convertible<pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long>>>(args_obj[2]) && is_convertible<pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long>>>(args_obj[3]) && is_convertible<pythonic::types::none_type>(args_obj[4]))
        return to_python(__for_method__OperatorsSphereHarmo2D__vsh_from_divrotsh5(from_python<pythonic::types::ndarray<double,pythonic::types::pshape<long>>>(args_obj[0]), from_python<long>(args_obj[1]), from_python<pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long>>>(args_obj[2]), from_python<pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long>>>(args_obj[3]), from_python<pythonic::types::none_type>(args_obj[4])));
    else {
        return nullptr;
    }
}

static PyObject *
__pythran_wrap___for_method__OperatorsSphereHarmo2D__vsh_from_divrotsh6(PyObject *self, PyObject *args, PyObject *kw)
{
    PyObject* args_obj[4+1];
    char const* keywords[] = {"self_inv_K2_r","self_nlm","div_lm","rot_lm", nullptr};
    if(! PyArg_ParseTupleAndKeywords(args, kw, "OOOO",
                                     (char**)keywords, &args_obj[0], &args_obj[1], &args_obj[2], &args_obj[3]))
        return nullptr;
    if(is_convertible<pythonic::types::ndarray<double,pythonic::types::pshape<long>>>(args_obj[0]) && is_convertible<long>(args_obj[1]) && is_convertible<pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long>>>(args_obj[2]) && is_convertible<pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long>>>(args_obj[3]))
        return to_python(__for_method__OperatorsSphereHarmo2D__vsh_from_divrotsh6(from_python<pythonic::types::ndarray<double,pythonic::types::pshape<long>>>(args_obj[0]), from_python<long>(args_obj[1]), from_python<pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long>>>(args_obj[2]), from_python<pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long>>>(args_obj[3])));
    else {
        return nullptr;
    }
}

static PyObject *
__pythran_wrap___for_method__OperatorsSphereHarmo2D__divrotsh_from_vsh0(PyObject *self, PyObject *args, PyObject *kw)
{
    PyObject* args_obj[6+1];
    char const* keywords[] = {"self_K2_r","self_nlm","uD_lm","uR_lm","div_lm","rot_lm", nullptr};
    if(! PyArg_ParseTupleAndKeywords(args, kw, "OOOOOO",
                                     (char**)keywords, &args_obj[0], &args_obj[1], &args_obj[2], &args_obj[3], &args_obj[4], &args_obj[5]))
        return nullptr;
    if(is_convertible<pythonic::types::ndarray<double,pythonic::types::pshape<long>>>(args_obj[0]) && is_convertible<long>(args_obj[1]) && is_convertible<pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long>>>(args_obj[2]) && is_convertible<pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long>>>(args_obj[3]) && is_convertible<pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long>>>(args_obj[4]) && is_convertible<pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long>>>(args_obj[5]))
        return to_python(__for_method__OperatorsSphereHarmo2D__divrotsh_from_vsh0(from_python<pythonic::types::ndarray<double,pythonic::types::pshape<long>>>(args_obj[0]), from_python<long>(args_obj[1]), from_python<pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long>>>(args_obj[2]), from_python<pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long>>>(args_obj[3]), from_python<pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long>>>(args_obj[4]), from_python<pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long>>>(args_obj[5])));
    else {
        return nullptr;
    }
}

static PyObject *
__pythran_wrap___for_method__OperatorsSphereHarmo2D__divrotsh_from_vsh1(PyObject *self, PyObject *args, PyObject *kw)
{
    PyObject* args_obj[6+1];
    char const* keywords[] = {"self_K2_r","self_nlm","uD_lm","uR_lm","div_lm","rot_lm", nullptr};
    if(! PyArg_ParseTupleAndKeywords(args, kw, "OOOOOO",
                                     (char**)keywords, &args_obj[0], &args_obj[1], &args_obj[2], &args_obj[3], &args_obj[4], &args_obj[5]))
        return nullptr;
    if(is_convertible<pythonic::types::ndarray<double,pythonic::types::pshape<long>>>(args_obj[0]) && is_convertible<long>(args_obj[1]) && is_convertible<pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long>>>(args_obj[2]) && is_convertible<pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long>>>(args_obj[3]) && is_convertible<pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long>>>(args_obj[4]) && is_convertible<pythonic::types::none_type>(args_obj[5]))
        return to_python(__for_method__OperatorsSphereHarmo2D__divrotsh_from_vsh1(from_python<pythonic::types::ndarray<double,pythonic::types::pshape<long>>>(args_obj[0]), from_python<long>(args_obj[1]), from_python<pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long>>>(args_obj[2]), from_python<pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long>>>(args_obj[3]), from_python<pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long>>>(args_obj[4]), from_python<pythonic::types::none_type>(args_obj[5])));
    else {
        return nullptr;
    }
}

static PyObject *
__pythran_wrap___for_method__OperatorsSphereHarmo2D__divrotsh_from_vsh2(PyObject *self, PyObject *args, PyObject *kw)
{
    PyObject* args_obj[5+1];
    char const* keywords[] = {"self_K2_r","self_nlm","uD_lm","uR_lm","div_lm", nullptr};
    if(! PyArg_ParseTupleAndKeywords(args, kw, "OOOOO",
                                     (char**)keywords, &args_obj[0], &args_obj[1], &args_obj[2], &args_obj[3], &args_obj[4]))
        return nullptr;
    if(is_convertible<pythonic::types::ndarray<double,pythonic::types::pshape<long>>>(args_obj[0]) && is_convertible<long>(args_obj[1]) && is_convertible<pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long>>>(args_obj[2]) && is_convertible<pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long>>>(args_obj[3]) && is_convertible<pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long>>>(args_obj[4]))
        return to_python(__for_method__OperatorsSphereHarmo2D__divrotsh_from_vsh2(from_python<pythonic::types::ndarray<double,pythonic::types::pshape<long>>>(args_obj[0]), from_python<long>(args_obj[1]), from_python<pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long>>>(args_obj[2]), from_python<pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long>>>(args_obj[3]), from_python<pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long>>>(args_obj[4])));
    else {
        return nullptr;
    }
}

static PyObject *
__pythran_wrap___for_method__OperatorsSphereHarmo2D__divrotsh_from_vsh3(PyObject *self, PyObject *args, PyObject *kw)
{
    PyObject* args_obj[6+1];
    char const* keywords[] = {"self_K2_r","self_nlm","uD_lm","uR_lm","div_lm","rot_lm", nullptr};
    if(! PyArg_ParseTupleAndKeywords(args, kw, "OOOOOO",
                                     (char**)keywords, &args_obj[0], &args_obj[1], &args_obj[2], &args_obj[3], &args_obj[4], &args_obj[5]))
        return nullptr;
    if(is_convertible<pythonic::types::ndarray<double,pythonic::types::pshape<long>>>(args_obj[0]) && is_convertible<long>(args_obj[1]) && is_convertible<pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long>>>(args_obj[2]) && is_convertible<pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long>>>(args_obj[3]) && is_convertible<pythonic::types::none_type>(args_obj[4]) && is_convertible<pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long>>>(args_obj[5]))
        return to_python(__for_method__OperatorsSphereHarmo2D__divrotsh_from_vsh3(from_python<pythonic::types::ndarray<double,pythonic::types::pshape<long>>>(args_obj[0]), from_python<long>(args_obj[1]), from_python<pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long>>>(args_obj[2]), from_python<pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long>>>(args_obj[3]), from_python<pythonic::types::none_type>(args_obj[4]), from_python<pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long>>>(args_obj[5])));
    else {
        return nullptr;
    }
}

static PyObject *
__pythran_wrap___for_method__OperatorsSphereHarmo2D__divrotsh_from_vsh4(PyObject *self, PyObject *args, PyObject *kw)
{
    PyObject* args_obj[6+1];
    char const* keywords[] = {"self_K2_r","self_nlm","uD_lm","uR_lm","div_lm","rot_lm", nullptr};
    if(! PyArg_ParseTupleAndKeywords(args, kw, "OOOOOO",
                                     (char**)keywords, &args_obj[0], &args_obj[1], &args_obj[2], &args_obj[3], &args_obj[4], &args_obj[5]))
        return nullptr;
    if(is_convertible<pythonic::types::ndarray<double,pythonic::types::pshape<long>>>(args_obj[0]) && is_convertible<long>(args_obj[1]) && is_convertible<pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long>>>(args_obj[2]) && is_convertible<pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long>>>(args_obj[3]) && is_convertible<pythonic::types::none_type>(args_obj[4]) && is_convertible<pythonic::types::none_type>(args_obj[5]))
        return to_python(__for_method__OperatorsSphereHarmo2D__divrotsh_from_vsh4(from_python<pythonic::types::ndarray<double,pythonic::types::pshape<long>>>(args_obj[0]), from_python<long>(args_obj[1]), from_python<pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long>>>(args_obj[2]), from_python<pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long>>>(args_obj[3]), from_python<pythonic::types::none_type>(args_obj[4]), from_python<pythonic::types::none_type>(args_obj[5])));
    else {
        return nullptr;
    }
}

static PyObject *
__pythran_wrap___for_method__OperatorsSphereHarmo2D__divrotsh_from_vsh5(PyObject *self, PyObject *args, PyObject *kw)
{
    PyObject* args_obj[5+1];
    char const* keywords[] = {"self_K2_r","self_nlm","uD_lm","uR_lm","div_lm", nullptr};
    if(! PyArg_ParseTupleAndKeywords(args, kw, "OOOOO",
                                     (char**)keywords, &args_obj[0], &args_obj[1], &args_obj[2], &args_obj[3], &args_obj[4]))
        return nullptr;
    if(is_convertible<pythonic::types::ndarray<double,pythonic::types::pshape<long>>>(args_obj[0]) && is_convertible<long>(args_obj[1]) && is_convertible<pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long>>>(args_obj[2]) && is_convertible<pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long>>>(args_obj[3]) && is_convertible<pythonic::types::none_type>(args_obj[4]))
        return to_python(__for_method__OperatorsSphereHarmo2D__divrotsh_from_vsh5(from_python<pythonic::types::ndarray<double,pythonic::types::pshape<long>>>(args_obj[0]), from_python<long>(args_obj[1]), from_python<pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long>>>(args_obj[2]), from_python<pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long>>>(args_obj[3]), from_python<pythonic::types::none_type>(args_obj[4])));
    else {
        return nullptr;
    }
}

static PyObject *
__pythran_wrap___for_method__OperatorsSphereHarmo2D__divrotsh_from_vsh6(PyObject *self, PyObject *args, PyObject *kw)
{
    PyObject* args_obj[4+1];
    char const* keywords[] = {"self_K2_r","self_nlm","uD_lm","uR_lm", nullptr};
    if(! PyArg_ParseTupleAndKeywords(args, kw, "OOOO",
                                     (char**)keywords, &args_obj[0], &args_obj[1], &args_obj[2], &args_obj[3]))
        return nullptr;
    if(is_convertible<pythonic::types::ndarray<double,pythonic::types::pshape<long>>>(args_obj[0]) && is_convertible<long>(args_obj[1]) && is_convertible<pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long>>>(args_obj[2]) && is_convertible<pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long>>>(args_obj[3]))
        return to_python(__for_method__OperatorsSphereHarmo2D__divrotsh_from_vsh6(from_python<pythonic::types::ndarray<double,pythonic::types::pshape<long>>>(args_obj[0]), from_python<long>(args_obj[1]), from_python<pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long>>>(args_obj[2]), from_python<pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long>>>(args_obj[3])));
    else {
        return nullptr;
    }
}

static PyObject *
__pythran_wrap___for_method__OperatorsSphereHarmo2D__invlaplacian_sh0(PyObject *self, PyObject *args, PyObject *kw)
{
    PyObject* args_obj[3+1];
    char const* keywords[] = {"self_inv_K2_not0","a_lm","negative", nullptr};
    if(! PyArg_ParseTupleAndKeywords(args, kw, "OOO",
                                     (char**)keywords, &args_obj[0], &args_obj[1], &args_obj[2]))
        return nullptr;
    if(is_convertible<pythonic::types::ndarray<double,pythonic::types::pshape<long>>>(args_obj[0]) && is_convertible<pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long>>>(args_obj[1]) && is_convertible<bool>(args_obj[2]))
        return to_python(__for_method__OperatorsSphereHarmo2D__invlaplacian_sh0(from_python<pythonic::types::ndarray<double,pythonic::types::pshape<long>>>(args_obj[0]), from_python<pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long>>>(args_obj[1]), from_python<bool>(args_obj[2])));
    else {
        return nullptr;
    }
}

static PyObject *
__pythran_wrap___for_method__OperatorsSphereHarmo2D__invlaplacian_sh1(PyObject *self, PyObject *args, PyObject *kw)
{
    PyObject* args_obj[2+1];
    char const* keywords[] = {"self_inv_K2_not0","a_lm", nullptr};
    if(! PyArg_ParseTupleAndKeywords(args, kw, "OO",
                                     (char**)keywords, &args_obj[0], &args_obj[1]))
        return nullptr;
    if(is_convertible<pythonic::types::ndarray<double,pythonic::types::pshape<long>>>(args_obj[0]) && is_convertible<pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long>>>(args_obj[1]))
        return to_python(__for_method__OperatorsSphereHarmo2D__invlaplacian_sh1(from_python<pythonic::types::ndarray<double,pythonic::types::pshape<long>>>(args_obj[0]), from_python<pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long>>>(args_obj[1])));
    else {
        return nullptr;
    }
}

static PyObject *
__pythran_wrap___for_method__OperatorsSphereHarmo2D__laplacian_sh0(PyObject *self, PyObject *args, PyObject *kw)
{
    PyObject* args_obj[3+1];
    char const* keywords[] = {"self_K2","a_lm","negative", nullptr};
    if(! PyArg_ParseTupleAndKeywords(args, kw, "OOO",
                                     (char**)keywords, &args_obj[0], &args_obj[1], &args_obj[2]))
        return nullptr;
    if(is_convertible<pythonic::types::ndarray<double,pythonic::types::pshape<long>>>(args_obj[0]) && is_convertible<pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long>>>(args_obj[1]) && is_convertible<bool>(args_obj[2]))
        return to_python(__for_method__OperatorsSphereHarmo2D__laplacian_sh0(from_python<pythonic::types::ndarray<double,pythonic::types::pshape<long>>>(args_obj[0]), from_python<pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long>>>(args_obj[1]), from_python<bool>(args_obj[2])));
    else {
        return nullptr;
    }
}

static PyObject *
__pythran_wrap___for_method__OperatorsSphereHarmo2D__laplacian_sh1(PyObject *self, PyObject *args, PyObject *kw)
{
    PyObject* args_obj[2+1];
    char const* keywords[] = {"self_K2","a_lm", nullptr};
    if(! PyArg_ParseTupleAndKeywords(args, kw, "OO",
                                     (char**)keywords, &args_obj[0], &args_obj[1]))
        return nullptr;
    if(is_convertible<pythonic::types::ndarray<double,pythonic::types::pshape<long>>>(args_obj[0]) && is_convertible<pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long>>>(args_obj[1]))
        return to_python(__for_method__OperatorsSphereHarmo2D__laplacian_sh1(from_python<pythonic::types::ndarray<double,pythonic::types::pshape<long>>>(args_obj[0]), from_python<pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long>>>(args_obj[1])));
    else {
        return nullptr;
    }
}

            static PyObject *
            __pythran_wrapall___for_method__OperatorsSphereHarmo2D__vsh_from_divrotsh(PyObject *self, PyObject *args, PyObject *kw)
            {
                return pythonic::handle_python_exception([self, args, kw]()
                -> PyObject* {

if(PyObject* obj = __pythran_wrap___for_method__OperatorsSphereHarmo2D__vsh_from_divrotsh0(self, args, kw))
    return obj;
PyErr_Clear();


if(PyObject* obj = __pythran_wrap___for_method__OperatorsSphereHarmo2D__vsh_from_divrotsh1(self, args, kw))
    return obj;
PyErr_Clear();


if(PyObject* obj = __pythran_wrap___for_method__OperatorsSphereHarmo2D__vsh_from_divrotsh2(self, args, kw))
    return obj;
PyErr_Clear();


if(PyObject* obj = __pythran_wrap___for_method__OperatorsSphereHarmo2D__vsh_from_divrotsh3(self, args, kw))
    return obj;
PyErr_Clear();


if(PyObject* obj = __pythran_wrap___for_method__OperatorsSphereHarmo2D__vsh_from_divrotsh4(self, args, kw))
    return obj;
PyErr_Clear();


if(PyObject* obj = __pythran_wrap___for_method__OperatorsSphereHarmo2D__vsh_from_divrotsh5(self, args, kw))
    return obj;
PyErr_Clear();


if(PyObject* obj = __pythran_wrap___for_method__OperatorsSphereHarmo2D__vsh_from_divrotsh6(self, args, kw))
    return obj;
PyErr_Clear();

                return pythonic::python::raise_invalid_argument(
                               "__for_method__OperatorsSphereHarmo2D__vsh_from_divrotsh", "\n""    - __for_method__OperatorsSphereHarmo2D__vsh_from_divrotsh(float64[:], int, complex128[:], complex128[:], complex128[:], complex128[:])\n""    - __for_method__OperatorsSphereHarmo2D__vsh_from_divrotsh(float64[:], int, complex128[:], complex128[:], complex128[:], NoneType)\n""    - __for_method__OperatorsSphereHarmo2D__vsh_from_divrotsh(float64[:], int, complex128[:], complex128[:], complex128[:])\n""    - __for_method__OperatorsSphereHarmo2D__vsh_from_divrotsh(float64[:], int, complex128[:], complex128[:], NoneType, complex128[:])\n""    - __for_method__OperatorsSphereHarmo2D__vsh_from_divrotsh(float64[:], int, complex128[:], complex128[:], NoneType, NoneType)\n""    - __for_method__OperatorsSphereHarmo2D__vsh_from_divrotsh(float64[:], int, complex128[:], complex128[:], NoneType)\n""    - __for_method__OperatorsSphereHarmo2D__vsh_from_divrotsh(float64[:], int, complex128[:], complex128[:])", args, kw);
                });
            }


            static PyObject *
            __pythran_wrapall___for_method__OperatorsSphereHarmo2D__divrotsh_from_vsh(PyObject *self, PyObject *args, PyObject *kw)
            {
                return pythonic::handle_python_exception([self, args, kw]()
                -> PyObject* {

if(PyObject* obj = __pythran_wrap___for_method__OperatorsSphereHarmo2D__divrotsh_from_vsh0(self, args, kw))
    return obj;
PyErr_Clear();


if(PyObject* obj = __pythran_wrap___for_method__OperatorsSphereHarmo2D__divrotsh_from_vsh1(self, args, kw))
    return obj;
PyErr_Clear();


if(PyObject* obj = __pythran_wrap___for_method__OperatorsSphereHarmo2D__divrotsh_from_vsh2(self, args, kw))
    return obj;
PyErr_Clear();


if(PyObject* obj = __pythran_wrap___for_method__OperatorsSphereHarmo2D__divrotsh_from_vsh3(self, args, kw))
    return obj;
PyErr_Clear();


if(PyObject* obj = __pythran_wrap___for_method__OperatorsSphereHarmo2D__divrotsh_from_vsh4(self, args, kw))
    return obj;
PyErr_Clear();


if(PyObject* obj = __pythran_wrap___for_method__OperatorsSphereHarmo2D__divrotsh_from_vsh5(self, args, kw))
    return obj;
PyErr_Clear();


if(PyObject* obj = __pythran_wrap___for_method__OperatorsSphereHarmo2D__divrotsh_from_vsh6(self, args, kw))
    return obj;
PyErr_Clear();

                return pythonic::python::raise_invalid_argument(
                               "__for_method__OperatorsSphereHarmo2D__divrotsh_from_vsh", "\n""    - __for_method__OperatorsSphereHarmo2D__divrotsh_from_vsh(float64[:], int, complex128[:], complex128[:], complex128[:], complex128[:])\n""    - __for_method__OperatorsSphereHarmo2D__divrotsh_from_vsh(float64[:], int, complex128[:], complex128[:], complex128[:], NoneType)\n""    - __for_method__OperatorsSphereHarmo2D__divrotsh_from_vsh(float64[:], int, complex128[:], complex128[:], complex128[:])\n""    - __for_method__OperatorsSphereHarmo2D__divrotsh_from_vsh(float64[:], int, complex128[:], complex128[:], NoneType, complex128[:])\n""    - __for_method__OperatorsSphereHarmo2D__divrotsh_from_vsh(float64[:], int, complex128[:], complex128[:], NoneType, NoneType)\n""    - __for_method__OperatorsSphereHarmo2D__divrotsh_from_vsh(float64[:], int, complex128[:], complex128[:], NoneType)\n""    - __for_method__OperatorsSphereHarmo2D__divrotsh_from_vsh(float64[:], int, complex128[:], complex128[:])", args, kw);
                });
            }


            static PyObject *
            __pythran_wrapall___for_method__OperatorsSphereHarmo2D__invlaplacian_sh(PyObject *self, PyObject *args, PyObject *kw)
            {
                return pythonic::handle_python_exception([self, args, kw]()
                -> PyObject* {

if(PyObject* obj = __pythran_wrap___for_method__OperatorsSphereHarmo2D__invlaplacian_sh0(self, args, kw))
    return obj;
PyErr_Clear();


if(PyObject* obj = __pythran_wrap___for_method__OperatorsSphereHarmo2D__invlaplacian_sh1(self, args, kw))
    return obj;
PyErr_Clear();

                return pythonic::python::raise_invalid_argument(
                               "__for_method__OperatorsSphereHarmo2D__invlaplacian_sh", "\n""    - __for_method__OperatorsSphereHarmo2D__invlaplacian_sh(float64[:], complex128[:], bool)\n""    - __for_method__OperatorsSphereHarmo2D__invlaplacian_sh(float64[:], complex128[:])", args, kw);
                });
            }


            static PyObject *
            __pythran_wrapall___for_method__OperatorsSphereHarmo2D__laplacian_sh(PyObject *self, PyObject *args, PyObject *kw)
            {
                return pythonic::handle_python_exception([self, args, kw]()
                -> PyObject* {

if(PyObject* obj = __pythran_wrap___for_method__OperatorsSphereHarmo2D__laplacian_sh0(self, args, kw))
    return obj;
PyErr_Clear();


if(PyObject* obj = __pythran_wrap___for_method__OperatorsSphereHarmo2D__laplacian_sh1(self, args, kw))
    return obj;
PyErr_Clear();

                return pythonic::python::raise_invalid_argument(
                               "__for_method__OperatorsSphereHarmo2D__laplacian_sh", "\n""    - __for_method__OperatorsSphereHarmo2D__laplacian_sh(float64[:], complex128[:], bool)\n""    - __for_method__OperatorsSphereHarmo2D__laplacian_sh(float64[:], complex128[:])", args, kw);
                });
            }


static PyMethodDef Methods[] = {
    {
    "__for_method__OperatorsSphereHarmo2D__vsh_from_divrotsh",
    (PyCFunction)__pythran_wrapall___for_method__OperatorsSphereHarmo2D__vsh_from_divrotsh,
    METH_VARARGS | METH_KEYWORDS,
    "Compute VSH from divergence and curl spherical harmonics ``div_lm``,\n""        ``rot_lm`` (``uD_lm`` and ``uR_lm`` are overwritten).\n""\n""    Supported prototypes:\n""\n""    - __for_method__OperatorsSphereHarmo2D__vsh_from_divrotsh(float64[:], int, complex128[:], complex128[:], complex128[:], complex128[:])\n""    - __for_method__OperatorsSphereHarmo2D__vsh_from_divrotsh(float64[:], int, complex128[:], complex128[:], complex128[:], NoneType)\n""    - __for_method__OperatorsSphereHarmo2D__vsh_from_divrotsh(float64[:], int, complex128[:], complex128[:], complex128[:])\n""    - __for_method__OperatorsSphereHarmo2D__vsh_from_divrotsh(float64[:], int, complex128[:], complex128[:], NoneType, complex128[:])\n""    - __for_method__OperatorsSphereHarmo2D__vsh_from_divrotsh(float64[:], int, complex128[:], complex128[:], NoneType, NoneType)\n""    - __for_method__OperatorsSphereHarmo2D__vsh_from_divrotsh(float64[:], int, complex128[:], complex128[:], NoneType)\n""    - __for_method__OperatorsSphereHarmo2D__vsh_from_divrotsh(float64[:], int, complex128[:], complex128[:])\n""\n"""},{
    "__for_method__OperatorsSphereHarmo2D__divrotsh_from_vsh",
    (PyCFunction)__pythran_wrapall___for_method__OperatorsSphereHarmo2D__divrotsh_from_vsh,
    METH_VARARGS | METH_KEYWORDS,
    "Compute divergence and curl from vector spherical harmonics uD, uR\n""        (``div_lm`` and ``rot_lm`` are overwritten).\n""\n""    Supported prototypes:\n""\n""    - __for_method__OperatorsSphereHarmo2D__divrotsh_from_vsh(float64[:], int, complex128[:], complex128[:], complex128[:], complex128[:])\n""    - __for_method__OperatorsSphereHarmo2D__divrotsh_from_vsh(float64[:], int, complex128[:], complex128[:], complex128[:], NoneType)\n""    - __for_method__OperatorsSphereHarmo2D__divrotsh_from_vsh(float64[:], int, complex128[:], complex128[:], complex128[:])\n""    - __for_method__OperatorsSphereHarmo2D__divrotsh_from_vsh(float64[:], int, complex128[:], complex128[:], NoneType, complex128[:])\n""    - __for_method__OperatorsSphereHarmo2D__divrotsh_from_vsh(float64[:], int, complex128[:], complex128[:], NoneType, NoneType)\n""    - __for_method__OperatorsSphereHarmo2D__divrotsh_from_vsh(float64[:], int, complex128[:], complex128[:], NoneType)\n""    - __for_method__OperatorsSphereHarmo2D__divrotsh_from_vsh(float64[:], int, complex128[:], complex128[:])\n""\n"""},{
    "__for_method__OperatorsSphereHarmo2D__invlaplacian_sh",
    (PyCFunction)__pythran_wrapall___for_method__OperatorsSphereHarmo2D__invlaplacian_sh,
    METH_VARARGS | METH_KEYWORDS,
    "Compute the Laplacian, :math:`\n""abla^{n} a^{lm}`\n""\n""    Supported prototypes:\n""\n""    - __for_method__OperatorsSphereHarmo2D__invlaplacian_sh(float64[:], complex128[:], bool)\n""    - __for_method__OperatorsSphereHarmo2D__invlaplacian_sh(float64[:], complex128[:])\n""\n""        Parameters\n""        ----------\n""        a_lm : ndarray\n""\n""        negative: bool, optional\n""            Negative of the result.\n""\n"""},{
    "__for_method__OperatorsSphereHarmo2D__laplacian_sh",
    (PyCFunction)__pythran_wrapall___for_method__OperatorsSphereHarmo2D__laplacian_sh,
    METH_VARARGS | METH_KEYWORDS,
    "Compute the Laplacian, :math:`\n""abla^{n} a^{lm}`\n""\n""    Supported prototypes:\n""\n""    - __for_method__OperatorsSphereHarmo2D__laplacian_sh(float64[:], complex128[:], bool)\n""    - __for_method__OperatorsSphereHarmo2D__laplacian_sh(float64[:], complex128[:])\n""\n""        Parameters\n""        ----------\n""        a_lm : ndarray\n""\n""        negative: bool, optional\n""            Negative of the result.\n""\n"""},
    {NULL, NULL, 0, NULL}
};


            #if PY_MAJOR_VERSION >= 3
              static struct PyModuleDef moduledef = {
                PyModuleDef_HEAD_INIT,
                "operators",            /* m_name */
                "",         /* m_doc */
                -1,                  /* m_size */
                Methods,             /* m_methods */
                NULL,                /* m_reload */
                NULL,                /* m_traverse */
                NULL,                /* m_clear */
                NULL,                /* m_free */
              };
            #define PYTHRAN_RETURN return theModule
            #define PYTHRAN_MODULE_INIT(s) PyInit_##s
            #else
            #define PYTHRAN_RETURN return
            #define PYTHRAN_MODULE_INIT(s) init##s
            #endif
            PyMODINIT_FUNC
            PYTHRAN_MODULE_INIT(operators)(void)
            #ifndef _WIN32
            __attribute__ ((visibility("default")))
            __attribute__ ((externally_visible))
            #endif
            ;
            PyMODINIT_FUNC
            PYTHRAN_MODULE_INIT(operators)(void) {
                import_array()
                #if PY_MAJOR_VERSION >= 3
                PyObject* theModule = PyModule_Create(&moduledef);
                #else
                PyObject* theModule = Py_InitModule3("operators",
                                                     Methods,
                                                     ""
                );
                #endif
                if(! theModule)
                    PYTHRAN_RETURN;
                PyObject * theDoc = Py_BuildValue("(sss)",
                                                  "0.9.3post1",
                                                  "2019-10-09 10:35:43.263287",
                                                  "ff9fa7955fa4005d60079ce294e740e2daca4e80e9c1f557dbef4ced20e6d8cc");
                if(! theDoc)
                    PYTHRAN_RETURN;
                PyModule_AddObject(theModule,
                                   "__pythran__",
                                   theDoc);

                PyModule_AddObject(theModule, "__transonic__", __transonic__);
PyModule_AddObject(theModule, "__code_new_method__OperatorsSphereHarmo2D__vsh_from_divrotsh", __code_new_method__OperatorsSphereHarmo2D__vsh_from_divrotsh);
PyModule_AddObject(theModule, "__code_new_method__OperatorsSphereHarmo2D__divrotsh_from_vsh", __code_new_method__OperatorsSphereHarmo2D__divrotsh_from_vsh);
PyModule_AddObject(theModule, "__code_new_method__OperatorsSphereHarmo2D__invlaplacian_sh", __code_new_method__OperatorsSphereHarmo2D__invlaplacian_sh);
PyModule_AddObject(theModule, "__code_new_method__OperatorsSphereHarmo2D__laplacian_sh", __code_new_method__OperatorsSphereHarmo2D__laplacian_sh);
                PYTHRAN_RETURN;
            }

#endif