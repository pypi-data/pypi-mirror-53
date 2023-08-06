
#include <x86intrin.h>
#include <stdint.h>

// gcc-9 -O3 -march=native bmi_intrin.c -fPIC -shared -o bmi_intrin.so

#define DEFMAP1_1(fnameExt, fnameInt, type) \
void fnameExt(void* inpv, void* oupv, int len) { \
  type* inp = (type*) inpv; \
  type* oup = (type*) oupv; \
  for (int i = 0; i < len; i++) { \
    oup[i] = fnameInt(inp[i]); \
  } \
}

#define DEFMAP1_1_3264(fnameExt, fnameIntPre) \
  DEFMAP1_1(fnameExt##32, fnameIntPre##32, uint32_t) \
  DEFMAP1_1(fnameExt##64, fnameIntPre##64, uint64_t)

DEFMAP1_1_3264(popcnt, _popcnt)
DEFMAP1_1_3264(lzcnt, _lzcnt_u)
DEFMAP1_1_3264(tzcnt, _tzcnt_u)
DEFMAP1_1_3264(blsi, _blsi_u)
DEFMAP1_1_3264(blsmsk, _blsmsk_u)
DEFMAP1_1_3264(blsr, _blsr_u)

#define DEFMAP2_1(fnameExt, fnameInt, type) \
void fnameExt(void* inp1v, void* inp2v, void* oupv, int len) { \
  type* inp1 = (type*) inp1v; \
  type* inp2 = (type*) inp2v; \
  type* oup = (type*) oupv; \
  for (int i = 0; i < len; i++) { \
    oup[i] = fnameInt(inp1[i], inp2[i]); \
  } \
} \
void fnameExt ## Bcast2(void* inp1v, void* inp2v, void* oupv, int len) { \
  type* inp1 = (type*) inp1v; \
  type in2 = *(type*) inp2v; \
  type* oup = (type*) oupv; \
  for (int i = 0; i < len; i++) { \
    oup[i] = fnameInt(inp1[i], in2); \
  } \
}

#define DEFMAP2_1_3264(fnameExt, fnameIntPre) \
  DEFMAP2_1(fnameExt##32, fnameIntPre##32, uint32_t) \
  DEFMAP2_1(fnameExt##64, fnameIntPre##64, uint64_t)

// DEFMAP2_1_3264(bextr2, _bextr2_u)
DEFMAP2_1_3264(bzhi, _bzhi_u)
DEFMAP2_1_3264(pdep, _pdep_u)
DEFMAP2_1_3264(pext, _pext_u)
