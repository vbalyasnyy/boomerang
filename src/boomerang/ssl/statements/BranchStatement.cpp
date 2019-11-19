#pragma region License
/*
 * This file is part of the Boomerang Decompiler.
 *
 * See the file "LICENSE.TERMS" for information on usage and
 * redistribution of this file, and for a DISCLAIMER OF ALL
 * WARRANTIES.
 */
#pragma endregion License
#include "BranchStatement.h"

#include "boomerang/db/IRFragment.h"
#include "boomerang/ssl/exp/Binary.h"
#include "boomerang/ssl/exp/Const.h"
#include "boomerang/ssl/exp/Terminal.h"
#include "boomerang/ssl/statements/StatementHelper.h"
#include "boomerang/ssl/type/BooleanType.h"
#include "boomerang/ssl/type/FloatType.h"
#include "boomerang/ssl/type/IntegerType.h"
#include "boomerang/util/log/Log.h"
#include "boomerang/visitor/expvisitor/ExpVisitor.h"
#include "boomerang/visitor/stmtexpvisitor/StmtExpVisitor.h"
#include "boomerang/visitor/stmtmodifier/StmtModifier.h"
#include "boomerang/visitor/stmtmodifier/StmtPartModifier.h"
#include "boomerang/visitor/stmtvisitor/StmtVisitor.h"

#include <QTextStreamManipulator>


BranchStatement::BranchStatement()
    : m_jumpType(BranchType::JE)
    , m_cond(nullptr)
    , m_isFloat(false)
{
    m_kind = StmtType::Branch;
}


BranchStatement::~BranchStatement()
{
}


void BranchStatement::setCondType(BranchType cond, bool usesFloat /*= false*/)
{
    m_jumpType = cond;
    m_isFloat  = usesFloat;

    // this is such a hack.. preferably we should actually recognise SUBFLAGS32(..,..,..) > 0
    // instead of just SUBFLAGS32(..,..,..) but I'll leave this in here for the moment as it
    // actually works.
    setCondExpr(Terminal::get(usesFloat ? opFflags : opFlags));
}


SharedExp BranchStatement::getCondExpr() const
{
    return m_cond;
}


void BranchStatement::setCondExpr(SharedExp pe)
{
    m_cond = pe;
}


IRFragment *BranchStatement::getFallBB() const
{
    if (!m_bb || m_bb->getNumSuccessors() != 2) {
        return nullptr;
    }

    return m_bb->getSuccessor(BELSE);
}


void BranchStatement::setFallBB(IRFragment *destBB)
{
    if (!m_bb || m_bb->getNumSuccessors() != 2) {
        return;
    }

    IRFragment *oldDestBB = m_bb->getSuccessor(BELSE);
    if (destBB != oldDestBB) {
        oldDestBB->removePredecessor(m_bb);
        m_bb->setSuccessor(BELSE, destBB);
        destBB->addPredecessor(m_bb);
    }
}


IRFragment *BranchStatement::getTakenBB() const
{
    if (!m_bb || m_bb->getNumSuccessors() != 2) {
        return nullptr;
    }

    return m_bb->getSuccessor(BTHEN);
}


void BranchStatement::setTakenBB(IRFragment *destBB)
{
    if (!m_bb || m_bb->getNumSuccessors() != 2) {
        return;
    }

    IRFragment *oldDestBB = m_bb->getSuccessor(BTHEN);
    if (destBB != oldDestBB) {
        oldDestBB->removePredecessor(m_bb);
        m_bb->setSuccessor(BTHEN, destBB);
        destBB->addPredecessor(m_bb);
    }
}


bool BranchStatement::search(const Exp &pattern, SharedExp &result) const
{
    if (m_cond) {
        return m_cond->search(pattern, result);
    }

    result = nullptr;
    return false;
}


bool BranchStatement::searchAndReplace(const Exp &pattern, SharedExp replace, bool cc)
{
    GotoStatement::searchAndReplace(pattern, replace, cc);
    bool change = false;

    if (m_cond) {
        m_cond = m_cond->searchReplaceAll(pattern, replace, change);
    }

    return change;
}


bool BranchStatement::searchAll(const Exp &pattern, std::list<SharedExp> &result) const
{
    if (m_cond) {
        return m_cond->searchAll(pattern, result);
    }

    return false;
}


void BranchStatement::print(OStream &os) const
{
    os << qSetFieldWidth(4) << m_number << qSetFieldWidth(0) << " ";
    os << "BRANCH ";

    if (m_dest == nullptr) {
        os << "*no dest*";
    }
    else if (!m_dest->isIntConst()) {
        os << m_dest;
    }
    else {
        // Really we'd like to display the destination label here...
        os << getFixedDest();
    }

    os << ", condition ";

    switch (m_jumpType) {
    case BranchType::JE: os << "equals"; break;
    case BranchType::JNE: os << "not equals"; break;
    case BranchType::JSL: os << "signed less"; break;
    case BranchType::JSLE: os << "signed less or equals"; break;
    case BranchType::JSGE: os << "signed greater or equals"; break;
    case BranchType::JSG: os << "signed greater"; break;
    case BranchType::JUL: os << "unsigned less"; break;
    case BranchType::JULE: os << "unsigned less or equals"; break;
    case BranchType::JUGE: os << "unsigned greater or equals"; break;
    case BranchType::JUG: os << "unsigned greater"; break;
    case BranchType::JMI: os << "minus"; break;
    case BranchType::JPOS: os << "plus"; break;
    case BranchType::JOF: os << "overflow"; break;
    case BranchType::JNOF: os << "no overflow"; break;
    case BranchType::JPAR: os << "parity"; break;
    case BranchType::JNPAR: os << "no parity"; break;
    case BranchType::INVALID: assert(false); break;
    }

    if (m_isFloat) {
        os << " float";
    }

    os << '\n';

    if (m_cond) {
        os << "High level: ";
        m_cond->print(os);
    }
}


SharedStmt BranchStatement::clone() const
{
    std::shared_ptr<BranchStatement> ret(new BranchStatement);

    ret->m_dest       = m_dest->clone();
    ret->m_isComputed = m_isComputed;
    ret->m_jumpType   = m_jumpType;
    ret->m_cond       = m_cond ? m_cond->clone() : nullptr;
    ret->m_isFloat    = m_isFloat;
    // Statement members
    ret->m_bb     = m_bb;
    ret->m_proc   = m_proc;
    ret->m_number = m_number;

    return ret;
}


bool BranchStatement::accept(StmtVisitor *visitor) const
{
    return visitor->visit(this);
}


void BranchStatement::simplify()
{
    if (m_cond) {
        if (condToRelational(m_cond, m_jumpType)) {
            m_isFloat = true;
        }
    }
}


bool BranchStatement::accept(StmtExpVisitor *v)
{
    bool visitChildren = true;
    bool ret           = v->visit(shared_from_this()->as<BranchStatement>(), visitChildren);

    if (!visitChildren) {
        return ret;
    }

    // Destination will always be a const for X86, so the below will never be used in practice
    if (ret && m_dest) {
        ret = m_dest->acceptVisitor(v->ev);
    }

    if (ret && m_cond) {
        ret = m_cond->acceptVisitor(v->ev);
    }

    return ret;
}


bool BranchStatement::accept(StmtPartModifier *v)
{
    bool visitChildren = true;
    v->visit(shared_from_this()->as<BranchStatement>(), visitChildren);

    if (m_dest && visitChildren) {
        m_dest = m_dest->acceptModifier(v->mod);
    }

    if (m_cond && visitChildren) {
        m_cond = m_cond->acceptModifier(v->mod);
    }

    return true;
}


bool BranchStatement::accept(StmtModifier *v)
{
    bool visitChildren;

    v->visit(shared_from_this()->as<BranchStatement>(), visitChildren);

    if (v->m_mod) {
        if (m_dest && visitChildren) {
            m_dest = m_dest->acceptModifier(v->m_mod);
        }

        if (m_cond && visitChildren) {
            m_cond = m_cond->acceptModifier(v->m_mod);
        }
    }

    return true;
}
