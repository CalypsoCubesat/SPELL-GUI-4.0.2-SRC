///////////////////////////////////////////////////////////////////////////////
//
// PACKAGE   : com.astra.ses.spell.language.common
// 
// FILE      : AbstractPythonGrammar.java
//
// DATE      : Apr 28, 2014
//
// Copyright (C) 2008, 2011 SES ENGINEERING, Luxembourg S.A.R.L.
//
// By using this software in any way, you are agreeing to be bound by
// the terms of this license.
//
// All rights reserved. This program and the accompanying materials
// are made available under the terms of the Eclipse Public License v1.0
// which accompanies this distribution, and is available at
// http://www.eclipse.org/legal/epl-v10.html
//
// NO WARRANTY
// EXCEPT AS EXPRESSLY SET FORTH IN THIS AGREEMENT, THE PROGRAM IS PROVIDED
// ON AN "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, EITHER
// EXPRESS OR IMPLIED INCLUDING, WITHOUT LIMITATION, ANY WARRANTIES OR
// CONDITIONS OF TITLE, NON-INFRINGEMENT, MERCHANTABILITY OR FITNESS FOR A
// PARTICULAR PURPOSE. Each Recipient is solely responsible for determining
// the appropriateness of using and distributing the Program and assumes all
// risks associated with its exercise of rights under this Agreement ,
// including but not limited to the risks and costs of program errors,
// compliance with applicable laws, damage to or loss of data, programs or
// equipment, and unavailability or interruption of operations.
//
// DISCLAIMER OF LIABILITY
// EXCEPT AS EXPRESSLY SET FORTH IN THIS AGREEMENT, NEITHER RECIPIENT NOR ANY
// CONTRIBUTORS SHALL HAVE ANY LIABILITY FOR ANY DIRECT, INDIRECT, INCIDENTAL,
// SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING WITHOUT LIMITATION
// LOST PROFITS), HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
// CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
// ARISING IN ANY WAY OUT OF THE USE OR DISTRIBUTION OF THE PROGRAM OR THE
// EXERCISE OF ANY RIGHTS GRANTED HEREUNDER, EVEN IF ADVISED OF THE
// POSSIBILITY OF SUCH DAMAGES.
//
// Contributors:
//    SES ENGINEERING - initial API and implementation and/or initial documentation
//
// PROJECT   : SPELL
//
// SUBPROJECT: SPELL DEV
//
///////////////////////////////////////////////////////////////////////////////
/**
 * Copyright (c) 2005-2011 by Appcelerator, Inc. All Rights Reserved.
 * Licensed under the terms of the Eclipse Public License (EPL).
 * Please see the license.txt included with this distribution for details.
 * Any modifications to this file must keep this entire header intact.
 */
package com.astra.ses.spell.language.common;

import java.util.List;

import com.astra.ses.spell.language.ParseException;
import com.astra.ses.spell.language.model.Node;
import com.astra.ses.spell.language.model.Token;

public abstract class AbstractPythonGrammar extends AbstractGrammarErrorHandlers implements ITreeConstants, IGrammar {

    public final static boolean DEFAULT_SEARCH_ON_LAST = false;

    /**
     * @return the token at the given location in the stack.
     */
    public abstract Token getToken(int i);

    /**
     * @return the list of special added to the token manager (used so that we
     * can add more info to it later on)
     */
    public abstract List<Object> getTokenSourceSpecialTokensList();

    /**
     * @return the last pos.
     */
    protected abstract Token getJJLastPos();

    protected Object temporaryToken;

    protected final boolean generateTree;

    protected final IPythonGrammarActions grammarActions;

    protected AbstractPythonGrammar(boolean generateTree) {
        this.generateTree = generateTree;
        if (generateTree) {
            grammarActions = new DefaultPythonGrammarActions(this);
        } else {
            grammarActions = new NullPythonGrammarActions();
        }
    }

    protected static WithNameInvalidException withNameInvalidException = new WithNameInvalidException(
            "With cannot be used as identifier when future with_statement is available.");

    /**
     * Opens a node scope
     * 
     * @param n the node marking the beginning of the scope.
     */
    protected final void jjtreeOpenNodeScope(Node n) {
    }

    /**
     * Closes a node scope
     * 
     * @param n the node that should have its scope closed.
     * @throws ParseException 
     */
    protected final void jjtreeCloseNodeScope(Node n) throws ParseException {
        grammarActions.jjtreeCloseNodeScope(n);
    }

    protected final AbstractJJTPythonGrammarState createJJTPythonGrammarState(Class<?> treeBuilderClass) {
        if (this.generateTree) {
            return new JJTPythonGrammarState(treeBuilderClass, this);
        } else {
            return new NullJJTPythonGrammarState();
        }
    }

    /**
     * Default: add after the previous found token
     */
    public static final int STRATEGY_ADD_AFTER_PREV = 0;

    /**
     * Add before the 'next token' strategy
     */
    public static final int STRATEGY_BEFORE_NEXT = 1;

}