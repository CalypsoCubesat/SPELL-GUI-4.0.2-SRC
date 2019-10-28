///////////////////////////////////////////////////////////////////////////////
//
// PACKAGE   : com.astra.ses.spell.language.common
// 
// FILE      : CtxVisitor.java
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
import com.astra.ses.spell.language.Visitor;
import com.astra.ses.spell.language.model.SimpleNode;
import com.astra.ses.spell.language.model.ast.Attribute;
import com.astra.ses.spell.language.model.ast.Call;
import com.astra.ses.spell.language.model.ast.List;
import com.astra.ses.spell.language.model.ast.Name;
import com.astra.ses.spell.language.model.ast.Starred;
import com.astra.ses.spell.language.model.ast.Subscript;
import com.astra.ses.spell.language.model.ast.Tuple;
import com.astra.ses.spell.language.model.ast.expr_contextType;

public final class CtxVisitor extends Visitor
{

	private int	ctx;

	public CtxVisitor()
	{
	}

	public void setParam(SimpleNode node) throws Exception
	{
		this.ctx = expr_contextType.Param;
		visit(node);
	}

	public void setKwOnlyParam(SimpleNode node) throws Exception
	{
		this.ctx = expr_contextType.KwOnlyParam;
		visit(node);
	}

	public void setStore(SimpleNode node) throws Exception
	{
		this.ctx = expr_contextType.Store;
		visit(node);
	}

	public void setStore(SimpleNode[] nodes) throws Exception
	{
		for (int i = 0; i < nodes.length; i++)
			setStore(nodes[i]);
	}

	public void setDelete(SimpleNode node) throws Exception
	{
		this.ctx = expr_contextType.Del;
		visit(node);
	}

	public void setDelete(SimpleNode[] nodes) throws Exception
	{
		for (int i = 0; i < nodes.length; i++)
			setDelete(nodes[i]);
	}

	public void setAugStore(SimpleNode node) throws Exception
	{
		this.ctx = expr_contextType.AugStore;
		visit(node);
	}

	public Object visitName(Name node) throws Exception
	{
		if (ctx == expr_contextType.Store)
		{
			if (node.reserved) { throw new ParseException(StringUtils.format(
			        "Cannot assign value to %s (because it's a keyword)", node.id), node); }
		}
		node.ctx = ctx;
		return null;
	}

	public Object visitStarred(Starred node) throws Exception
	{
		node.ctx = ctx;
		traverse(node);
		return null;
	}

	public Object visitAttribute(Attribute node) throws Exception
	{
		node.ctx = ctx;
		return null;
	}

	public Object visitSubscript(Subscript node) throws Exception
	{
		node.ctx = ctx;
		return null;
	}

	public Object visitList(List node) throws Exception
	{
		if (ctx == expr_contextType.AugStore) { throw new ParseException("augmented assign to list not possible", node); }
		node.ctx = ctx;
		traverse(node);
		return null;
	}

	public Object visitTuple(Tuple node) throws Exception
	{
		if (ctx == expr_contextType.AugStore) { throw new ParseException("augmented assign to tuple not possible", node); }
		node.ctx = ctx;
		traverse(node);
		return null;
	}

	public Object visitCall(Call node) throws Exception
	{
		throw new ParseException("can't assign to function call", node);
	}

	public Object visitListComp(Call node) throws Exception
	{
		throw new ParseException("can't assign to list comprehension call", node);
	}

	public Object unhandled_node(SimpleNode node) throws Exception
	{
		throw new ParseException("can't assign to operator:" + node, node);
	}
}
