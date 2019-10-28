///////////////////////////////////////////////////////////////////////////////
//
// PACKAGE   : com.astra.ses.spell.language.common
// 
// FILE      : AbstractGrammarErrorHandlers.java
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

import java.util.ArrayList;
import java.util.List;

import com.astra.ses.spell.language.ParseException;
import com.astra.ses.spell.language.model.Token;

/**
 * This class contains the error-handling utilities.
 * 
 * @author Fabio
 */
public abstract class AbstractGrammarErrorHandlers extends AbstractGrammarWalkHelpers
{

	/**
	 * This marks the column where the last suite started.
	 */
	protected int	lastSuiteStartCol	= -1;

	/**
	 * Keep track of the parse exceptions (to keep from recursing in any
	 * situation)
	 */
	protected int	parseExceptions	  = 0;

	/**
	 * This method should be called when the current token marks a compound
	 * statement start E.g.: right after an if, for, while, etc.
	 */
	protected final void markLastAsSuiteStart()
	{
		Token currentToken = this.getCurrentToken();
		this.lastSuiteStartCol = currentToken.beginColumn;
	}

	/**
	 * @return the actual jjtree used to build the nodes (tree)
	 */
	protected abstract AbstractJJTPythonGrammarState getJJTree();

	/**
	 * List with the errors we handled during the parsing
	 */
	private final List<ParseException>	parseErrors	= new ArrayList<ParseException>();

	/**
	 * @return a list with the parse errors. Note that the returned value is not
	 *         a copy, but the actual internal list used to store the errors.
	 */
	public List<ParseException> getParseErrors()
	{
		return parseErrors;
	}

	/**
	 * Adds some parse exception to the list of parse exceptions found.
	 */
	private void addParseError(ParseException e)
	{
		parseErrors.add(e);
	}

	/**
	 * @return the 1st error that happened while parsing (or null if no error
	 *         happened)
	 */
	public Throwable getErrorOnParsing()
	{
		if (this.parseErrors != null && this.parseErrors.size() > 0) { return this.parseErrors.get(0); }
		return null;
	}

	// ---------------------------- Helpers to handle errors in the grammar.

	public final void addAndReport(ParseException e, String msg) throws ParseException
	{
		addParseError(e);
		parseExceptions++;
		if (parseExceptions > 100)
		{ // too many errors in the file... just stop trying to fix it (we could
		  // be recursing too)
			throw e;
		}
	}

	/**
	 * Called when there was an error trying to indent.
	 */
	protected final void handleErrorInIndent(ParseException e) throws ParseException
	{
		addAndReport(e, "Handle no indent");

		TokensIterator iterTokens = this.getTokensIterator(getCurrentToken(), 3, false);
		iterTokens.next(); // discard the curr
		if (!iterTokens.hasNext()) { throw new EmptySuiteException(); }
		Token nextToken = iterTokens.next();
		if (nextToken.beginColumn <= lastSuiteStartCol) { throw new EmptySuiteException(); }
	}

	/**
	 * Called when there was an error trying to indent.
	 */
	protected final void handleNoEof(ParseException e) throws ParseException
	{
		addAndReport(e, "Handle no EOF");
	}

	/**
	 * Called when there was an error trying to resolve an import
	 */
	protected final void handleErrorInImport(ParseException e) throws ParseException
	{
		addAndReport(e, "Handle error in import");
	}

	/**
	 * Happens when we could find a parenthesis close (so, we don't create it),
	 * but it's not the current, so, we have an error making the match.
	 */
	protected final void handleRParensNearButNotCurrent(ParseException e) throws ParseException
	{
		addAndReport(e, "Handle parens near but not current");
		Token t = getCurrentToken();

		AbstractTokenManager tokenManager = getTokenManager();
		final int rparenId = tokenManager.getRparenId();
		while (t != null && t.kind != rparenId)
		{
			t = t.next;
		}
		if (t != null && t.kind == rparenId)
		{
			// found it
			setCurrentToken(t);
		}
	}

	/**
	 * Called when there was an error trying to dedent. At this point, we must
	 * try to sync it to an actual dedent.
	 */
	protected final void handleErrorInDedent(ParseException e) throws ParseException
	{
		addAndReport(e, "Handle dedent");
		// lot's of tokens, but we'll bail out on an indent, so, that's OK.
		AbstractTokenManager tokenManager = getTokenManager();
		int indentId = tokenManager.getIndentId();
		int dedentId = tokenManager.getDedentId();

		int level = 0;

		// lot's of tokens, but we'll bail out on an indent, so, that's OK.
		TokensIterator iterTokens = this.getTokensIterator(getCurrentToken(), 50, false);
		while (iterTokens.hasNext())
		{
			Token next = iterTokens.next();
			if (level == 0)
			{
				// we can only do it if we're in the same level we started.
				if (next.kind == dedentId)
				{
					setCurrentToken(next);
					break;
				}
			}
			if (next.kind == indentId)
			{
				level += 1;
			}
			else if (next.kind == dedentId)
			{
				level -= 1;
			}
		}
	}

	protected final void handleErrorInStmt(ParseException e) throws ParseException
	{
		addAndReport(e, "Handle error in stmt");
	}

	/**
	 * Called when there was an error while resolving a statement.
	 */
	protected final void handleErrorInCompountStmt(ParseException e) throws ParseException
	{
		addAndReport(e, "Handle error in compount stmt");
	}

	/**
	 * Called when there was an error while resolving a statement.
	 */
	protected final void handleNoNewline(ParseException e) throws ParseException
	{
		addAndReport(e, "Handle no newline");
	}

	/**
	 * Called when there was an error because the value for a given key was not
	 * found.
	 */
	protected final void handleNoValInDict(ParseException e) throws ParseException
	{
		addAndReport(e, "No value for dict key");
	}

	/**
	 * This is called when recognized an indent but the new line was not
	 * recognized.
	 */
	protected final void handleNoNewlineInSuiteFound() throws ParseException
	{
		addAndReport(new ParseException("No new line found.", getCurrentToken()), "Handle no new line in suite");
	}

	protected final void handleNoSuiteMatch(ParseException e) throws ParseException
	{
		addAndReport(e, "Handle no suite match");
	}

	/**
	 * Called when there was an error trying to indent.
	 * 
	 * Actually creates a name so that the parsing can continue.
	 */
	protected final Token handleErrorInName(ParseException e) throws ParseException
	{
		addAndReport(e, "Handle name");
		Token currentToken = getCurrentToken();

		return this.getTokenManager().createFrom(currentToken, this.getTokenManager().getNameId(), "!<MissingName>!");
	}

}
