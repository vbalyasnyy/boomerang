#define sign_extend(N, SIZE)  Util::signExtend(N, SIZE)
#include <assert.h>

// #line 2 "machine/mips/disassembler.m"

/****************************************************************
 *
 * FILENAME
 *
 *   \file disassembler.cpp
 *
 * PURPOSE
 *
 *   Skeleton for MIPS disassembly
 *
 * AUTHOR
 *
 *   \author Markus Gothe, nietzsche@lysator.liu.se
 *
 * REVISION
 *
 *   $Id$
 *
 *****************************************************************/

#include "boomerang/global.h"
#include "boomerang/include/decoder.h"
