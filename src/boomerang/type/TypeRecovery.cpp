#include "TypeRecovery.h"

#include "boomerang/core/Boomerang.h"
#include "boomerang/db/proc/UserProc.h"
#include "boomerang/db/Prog.h"
#include "boomerang/util/Log.h"


void TypeRecoveryCommon::recoverProgramTypes(Prog *v)
{
    if (DEBUG_TA) {
        LOG_VERBOSE("=== start %1 type analysis ===", name());
    }

    // FIXME: This needs to be done in bottom-up order of the call-tree first,
    // repeating until no changes for cycles in the call graph
    for (Module *module : v->getModuleList()) {
        for (Function *pp : *module) {
            UserProc *proc = dynamic_cast<UserProc *>(pp);

            if ((nullptr == proc) || !proc->isDecoded()) {
                continue;
            }

            // FIXME: this just does local TA again. Need to resolve types for all parameter/arguments,
            // and return/results! This will require a "repeat until no change" loop
            LOG_VERBOSE("Global type analysis for %1", proc->getName());
            recoverFunctionTypes(pp);
        }
    }

    if (DEBUG_TA) {
        LOG_VERBOSE("=== end type analysis ===");
    }
}