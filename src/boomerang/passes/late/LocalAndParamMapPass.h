#pragma region License
/*
 * This file is part of the Boomerang Decompiler.
 *
 * See the file "LICENSE.TERMS" for information on usage and
 * redistribution of this file, and for a DISCLAIMER OF ALL
 * WARRANTIES.
 */
#pragma endregion License
#pragma once


#include "boomerang/passes/Pass.h"


/// Map expressions to locals and initial parameters
class LocalAndParamMapPass final : public IPass
{
public:
    LocalAndParamMapPass();

public:
    /// \copydoc IPass::execute
    bool execute(UserProc *proc) override;
};
