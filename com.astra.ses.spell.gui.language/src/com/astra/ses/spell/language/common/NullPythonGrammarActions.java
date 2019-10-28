///////////////////////////////////////////////////////////////////////////////
//
// PACKAGE   : com.astra.ses.spell.language.common
// 
// FILE      : NullPythonGrammarActions.java
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

import com.astra.ses.spell.language.ParseException;
import com.astra.ses.spell.language.model.ISpecialStr;
import com.astra.ses.spell.language.model.Node;
import com.astra.ses.spell.language.model.SimpleNode;
import com.astra.ses.spell.language.model.Token;
import com.astra.ses.spell.language.model.ast.Num;
import com.astra.ses.spell.language.model.ast.Str;

public final class NullPythonGrammarActions implements IPythonGrammarActions
{

	public void markDecoratorWithCall()
	{
	}

	public ISpecialStr convertStringToSpecialStr(Object o) throws ParseException
	{
		return null;
	}

	public void addToPeekCallFunc(Object t, boolean after)
	{

	}

	public void addSpecialTokenToLastOpened(Object o) throws ParseException
	{

	}

	@SuppressWarnings("rawtypes")
	public void addToPeek(SimpleNode peeked, Object t, boolean after, Class class_) throws ParseException
	{

	}

	@SuppressWarnings("rawtypes")
	public SimpleNode addToPeek(Object t, boolean after, Class class_) throws ParseException
	{
		return null;
	}

	public void jjtreeCloseNodeScope(Node n) throws ParseException
	{

	}

	public void addSpecialToken(Object o, int strategy) throws ParseException
	{

	}

	public void addSpecialToken(Object o) throws ParseException
	{

	}

	public void makeFloat(Token t, Num numberToFill) throws ParseException
	{

	}

	public void makeLong(Token t, Num numberToFill) throws ParseException
	{

	}

	public void makeComplex(Token t, Num numberToFill) throws ParseException
	{

	}

	public void makeString(Token t, int quotes, Str strToFill)
	{

	}

	public void findTokenAndAdd(String token) throws ParseException
	{

	}

	public void addSpecialToPrev(Object special, boolean after)
	{

	}

	public ISpecialStr createSpecialStr(String token) throws ParseException
	{

		return null;
	}

	public ISpecialStr createSpecialStr(String token, boolean searchOnLast) throws ParseException
	{

		return null;
	}

	public ISpecialStr createSpecialStr(String token, boolean searchOnLast, boolean throwException) throws ParseException
	{

		return null;
	}

	public void addToPeek(Object t, boolean after) throws ParseException
	{

	}

	public void makeInt(Token t, int radix, Token token, Num numberToFill) throws ParseException
	{

	}

	public void makeIntSub2(Token t, int radix, Token token, Num numberToFill) throws ParseException
	{

	}

	public void makeIntSub2CheckingOct(Token t, int radix, Token token, Num numberToFill) throws ParseException
	{
	}

	public void setImportFromLevel(int level)
	{

	}

}
