#pragma once

/*
 * Copyright (C) 2002, Trent Waddington
 *
 * See the file "LICENSE.TERMS" for information on usage and
 * redistribution of this file, and for a DISCLAIMER OF ALL
 * WARRANTIES.
 *
 */

#include <QTextStream>

#include "boomerang/db/exp/Exp.h"
#include "boomerang/db/Managed.h"

class Prog;
class Module;
class UserProc;
class Function;

/**
 * Base class for generating high-level code from statements.
 *
 * This class is provides methods which are generic of procedural
 * languages like C, Pascal, Fortranmake, etc. Included in the base class
 * is the follow and goto sets which are used during code generation.
 * Concrete implementations of this class provide specific language
 * bindings for a single procedure in the program.
 */
class ICodeGenerator
{
public:
    ICodeGenerator() {}
    virtual ~ICodeGenerator() {}

    /// Generate code for \p program to \p os.
    virtual void generateCode(const Prog* program, QTextStream& os) = 0;

    /**
     * Generate code for a module or function, or all modules.
     * \param program The program to generate code for.
     * \param cluster The cluster to generate code for, or nullptr to generate code for all clusters.
     * \param proc The function to generate code for, or nullptr to generate code for all procedures in a module.
     * \param intermixRTL Set this to true to intermix code with underlying intermediate representation.
     *                    Currently not implemented.
     */
    virtual void generateCode(const Prog* program, Module *cluster = nullptr, UserProc *proc = nullptr, bool intermixRTL = false) = 0;

public:
    /*
     * Functions to add new code, pure virtual.
     * DEPRECATED
     */
    // sequential statements

    /// Add an assignment statement at the current position.
    virtual void addAssignmentStatement(Assign *s) = 0;

    /**
     * Adds a call to the function \p proc.
     *
     * \param proc            The Proc the call is to.
     * \param name            The name the Proc has.
     * \param args            The arguments to the call.
     * \param results        The variable that will receive the return value of the function.
     *
     * \todo                Remove the \p name parameter and use Proc::getName()
     * \todo                Add assingment for when the function returns a struct.
     */
    virtual void addCallStatement(Function *proc, const QString& name, StatementList& args,
                                  StatementList *results) = 0;

    /**
     * Adds an indirect call to \a exp.
     * \see AddCallStatement
     * \param results UNUSED
     * \todo Add the use of \a results like AddCallStatement.
     */
    virtual void addIndCallStatement(const SharedExp& exp, StatementList& args, StatementList *results) = 0;

    /**
     * Adds a return statement and returns the first expression in \a rets.
     * \todo This should be returning a struct if more than one real return value.
     */
    virtual void addReturnStatement(StatementList *rets) = 0;

    /// Removes unused labels from the code.
    virtual void removeUnusedLabels(int maxOrd)  = 0;
};