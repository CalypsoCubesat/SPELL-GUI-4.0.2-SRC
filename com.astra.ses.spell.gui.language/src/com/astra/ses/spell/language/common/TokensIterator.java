///////////////////////////////////////////////////////////////////////////////
//
// PACKAGE   : com.astra.ses.spell.language.common
// 
// FILE      : TokensIterator.java
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

import java.util.HashSet;
import java.util.Iterator;
import java.util.NoSuchElementException;

import com.astra.ses.spell.language.model.Token;

/**
 * A helper iterator class that can look ahead x tokens breaking when some new
 * compound context starts (if wanted)
 */
final class TokensIterator implements Iterator<Token>
{

	private Token	               currentToken;
	private int	                   tokensToIterate;
	private int	                   tokensIterated;
	private boolean	               breakOnIndentsDedentsAndNewCompounds;
	private ITokenManager	       tokenManager;
	private Tuple<Token, Token>	   prevAndReturned;
	private final HashSet<Integer>	contextsToBreak	= new HashSet<Integer>();
	private boolean	               calculatedNext;
	private boolean	               isFirst;

	// private int parensLevel=0;

	/**
	 * @param firstIterationToken
	 *            this will be the 1st token returned in the iteration, and the
	 *            next token can be the next token already set in the given
	 *            token or a new token loaded from the manager.
	 * 
	 * @param tokensToIterate
	 *            if 1, will only yield 1 token, if 2, can get up to 2 tokens
	 *            and so on.
	 * 
	 * @param breakOnIndentsDedentsAndNewCompounds
	 *            if true, it'll break whenever we find a new compound context,
	 *            or an indent or dedent.
	 * 
	 * @return an iterator that'll iterate through the next tokens.
	 */
	public TokensIterator(ITokenManager tokenManager, Token firstIterationToken, int tokensToIterate,
	        boolean breakOnIndentsDedentsAndNewCompounds)
	{
		contextsToBreak.add(tokenManager.getIndentId());
		contextsToBreak.add(tokenManager.getDedentId());

		contextsToBreak.add(tokenManager.getIfId());
		contextsToBreak.add(tokenManager.getWhileId());
		contextsToBreak.add(tokenManager.getForId());
		contextsToBreak.add(tokenManager.getTryId());

		contextsToBreak.add(tokenManager.getDefId());
		contextsToBreak.add(tokenManager.getClassId());
		contextsToBreak.add(tokenManager.getAtId());

		reset(tokenManager, firstIterationToken, tokensToIterate, breakOnIndentsDedentsAndNewCompounds);
	}

	public void reset(ITokenManager tokenManager, Token firstIterationToken, int tokensToIterate,
	        boolean breakOnIndentsDedentsAndNewCompounds)
	{
		this.currentToken = firstIterationToken;
		this.tokenManager = tokenManager;
		this.tokensToIterate = tokensToIterate;
		this.breakOnIndentsDedentsAndNewCompounds = breakOnIndentsDedentsAndNewCompounds;
		this.tokensIterated = 0;
		this.tokensToIterate = 0;
		this.prevAndReturned = new Tuple<Token, Token>(null, null);
		this.calculatedNext = false;
		this.isFirst = true;
		// this.parensLevel = 0;
	}

	public boolean hasNext()
	{
		if (isFirst) { return currentToken != null; }
		if (!calculatedNext)
		{
			calculateNext();
			calculatedNext = true;
		}
		return currentToken != null && currentToken.next != null;
	}

	public Token next()
	{
		if (isFirst)
		{
			isFirst = false;
			return currentToken;
		}
		if (!calculatedNext)
		{
			calculateNext();
		}

		calculatedNext = false;
		tokensIterated += 1;
		if (currentToken == null || currentToken.next == null) { throw new NoSuchElementException(); }
		prevAndReturned.o1 = prevAndReturned.o2;
		prevAndReturned.o2 = currentToken.next;

		if (tokensIterated == tokensToIterate)
		{
			currentToken = null;
		}
		else
		{
			if (currentToken != null && currentToken.kind == tokenManager.getEofId())
			{
				// always break on EOF
				currentToken = null;

			}
			else if (breakOnIndentsDedentsAndNewCompounds)
			{
				if (currentToken != null && contextsToBreak.contains(currentToken.kind))
				{
					currentToken = null; // we must break it now (indent or
										 // dedent found)
				}
			}
		}
		if (currentToken != null)
		{
			currentToken = currentToken.next;
		}
		return prevAndReturned.o2;
	}

	private void calculateNext()
	{
		if (currentToken == null) { return; }

		if (currentToken.kind == tokenManager.getEofId())
		{
			// found end of file!
			currentToken = null;
			return;
		}

		if (currentToken.next == null)
		{
			currentToken.next = AbstractGrammarWalkHelpers.nextTokenConsideringNewLine(tokenManager);
			// if(currentToken.next != null){
			// int id = currentToken.next.kind;
			// if(id == tokenManager.getIndentId()){
			//
			// } else if(id == tokenManager.getRparenId() || id ==
			// tokenManager.getRbracketId() || id ==
			// tokenManager.getRbraceId()){
			// parensLevel--;
			//
			// }else if(id == tokenManager.getLparenId() || id ==
			// tokenManager.getLbracketId() || id ==
			// tokenManager.getLbraceId()){
			// parensLevel++;
			// }
			// }
		}

	}

	public void remove()
	{
		throw new RuntimeException("Not implemented");
	}

	public Token getBeforeLastReturned()
	{
		return this.prevAndReturned.o1;
	}

}
