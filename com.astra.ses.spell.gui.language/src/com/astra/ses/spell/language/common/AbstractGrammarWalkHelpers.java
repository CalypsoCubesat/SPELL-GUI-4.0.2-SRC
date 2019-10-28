///////////////////////////////////////////////////////////////////////////////
//
// PACKAGE   : com.astra.ses.spell.language.common
// 
// FILE      : AbstractGrammarWalkHelpers.java
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

import java.io.IOException;

import com.astra.ses.spell.language.model.Token;

/**
 * Helpers to walk through the grammar.
 * 
 * @author Fabio
 */
public abstract class AbstractGrammarWalkHelpers {

    private AbstractTokenManager tokenManager;

    /**
     * An iterator that can pass through the next tokens considering indentation.
     */
    private TokensIterator tokensIterator;

    /**
     * @return The token manager.
     */
    protected final AbstractTokenManager getTokenManager() {
        if (this.tokenManager == null) {
            this.tokenManager = (AbstractTokenManager) Reflection.getAttrObj(this, "token_source", true);
        }
        return this.tokenManager;
    }

    /**
     * @return the current token
     */
    protected abstract Token getCurrentToken();

    /**
     * Sets the current token in the grammar.
     */
    protected abstract void setCurrentToken(Token t);

    /**
     * @return the next available token considering new lines (just doing a getToken at any place won't always give us
     * the effect we'd usually expect -- which is finding new lines and indent tokens)
     */
    protected static Token nextTokenConsideringNewLine(ITokenManager tokenManager) {
        boolean foundNewLine = searchNewLine(tokenManager, true);
        if (foundNewLine) {
            tokenManager.indenting(0);
        }
        final Token nextToken = tokenManager.getNextToken();
        return nextToken;
    }

    /**
     * Searches for a new line in the input stream. If found, it'll stop right after it, otherwise, the stream will be
     * backed up the number of chars that've been read.
     */
    protected static boolean searchNewLine(ITokenManager tokenManager, boolean breakOnFirstNotWhitespace) {
        boolean foundNewLine = false;
        FastCharStream inputStream = tokenManager.getInputStream();
        int currentPos = inputStream.getCurrentPos();

        try {
            while (true) {
                try {
                    char c = inputStream.readChar();
                    if (c == '\r' || c == '\n') {
                        if (c == '\r') {
                            c = inputStream.readChar();
                            if (c != '\n') {
                                inputStream.backup(1);
                            }
                        }
                        foundNewLine = true;
                        break;
                    }
                    if (breakOnFirstNotWhitespace && !Character.isWhitespace(c)) {
                        break;
                    }
                } catch (IOException e) {
                    break;
                }
            }
        } finally {
            if (!foundNewLine) {
                inputStream.restorePos(currentPos);
            }
        }
        return foundNewLine;
    }

    /**
     * @see TokensIterator#TokensIterator(AbstractTokenManager, Token, int, boolean)
     * 
     * Note that if one request is done, another cannot be done and use the iterator, because
     * the same instance is used over and over!
     */
    protected final TokensIterator getTokensIterator(Token firstIterationToken, int tokensToIterate,
            boolean breakOnIndentsDedentsAndNewCompounds) {
        if (this.tokensIterator == null) {
            this.tokensIterator = new TokensIterator(getTokenManager(), firstIterationToken, tokensToIterate,
                    breakOnIndentsDedentsAndNewCompounds);
        } else {
            this.tokensIterator.reset(getTokenManager(), firstIterationToken, tokensToIterate,
                    breakOnIndentsDedentsAndNewCompounds);
        }
        return this.tokensIterator;
    }
}
