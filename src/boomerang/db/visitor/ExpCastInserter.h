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


#include "boomerang/db/visitor/ExpModifier.h"


class UserProc;

using SharedType = std::shared_ptr<class Type>;


/**
 *
 */
class ExpCastInserter : public ExpModifier
{
public:
    ExpCastInserter() = default;

    /// Check the type of the address expression of memof to make sure it is compatible with the given memofType.
    /// memof may be changed internally to include a TypedExp, which will emit as a cast
    static void checkMemofType(const SharedExp& memof, SharedType memofType);

    /// \copydoc ExpModifier::preVisit
    /// Don't consider if already cast
    SharedExp preVisit(const std::shared_ptr<TypedExp>& exp, bool& visitChildren) override;

    /// \copydoc ExpModifier::postVisit
    SharedExp postVisit(const std::shared_ptr<RefExp>& exp) override;

    /// \copydoc ExpModifier::postVisit
    SharedExp postVisit(const std::shared_ptr<Binary>& exp) override;

    /// \copydoc ExpModifier::postVisit
    SharedExp postVisit(const std::shared_ptr<Const>& exp) override;

};
