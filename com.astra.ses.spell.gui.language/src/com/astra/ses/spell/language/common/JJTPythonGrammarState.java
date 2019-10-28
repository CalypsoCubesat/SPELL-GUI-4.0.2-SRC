///////////////////////////////////////////////////////////////////////////////
//
// PACKAGE   : com.astra.ses.spell.language.common
// 
// FILE      : JJTPythonGrammarState.java
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

import java.lang.reflect.Constructor;

import com.astra.ses.spell.language.ParseException;
import com.astra.ses.spell.language.model.Node;
import com.astra.ses.spell.language.model.SimpleNode;
import com.astra.ses.spell.language.model.Token;

public final class JJTPythonGrammarState extends AbstractJJTPythonGrammarState implements IJJTPythonGrammarState
{
	protected final FastStack<SimpleNode>	nodes;
	protected final IntStack	          marks;
	protected final IntStack	          lines;
	protected final IntStack	          columns;

	protected int	                      sp;	             // number of nodes
															 // on stack
	protected int	                      mk;	             // current mark
	protected boolean	                  node_created;

	private final AbstractPythonGrammar	  grammar;

	public JJTPythonGrammarState(Class<?> treeBuilderClass, AbstractPythonGrammar grammar)
	{
		this.grammar = grammar;
		nodes = new FastStack<SimpleNode>(73);
		marks = new IntStack();
		lines = new IntStack();
		columns = new IntStack();
		sp = 0;
		mk = 0;

		try
		{
			Constructor<?> constructor = treeBuilderClass.getConstructor(JJTPythonGrammarState.class);
			this.builder = (ITreeBuilder) constructor.newInstance(new Object[] { this });
		}
		catch (Exception e)
		{
			throw new RuntimeException(e);
		}
	}

	public AbstractPythonGrammar getGrammar()
	{
		return grammar;
	}

	@Override
	public final SimpleNode getLastOpened()
	{
		return this.builder.getLastOpened();
	}

	/* Pushes a node on to the stack. */
	private void pushNode(Node n, SimpleNode created, int line, int col)
	{
		nodes.push(created);

		if (created.beginLine == 0) created.beginLine = line;

		if (created.beginColumn == 0) created.beginColumn = col;

		++sp;
	}

	/**
	 * Note that popNode doesn't pop lines and columns. This is because those
	 * are always controlled by the openNodeScope/closeNodeScope or
	 * openNodeScope/clearNodeScope.
	 * 
	 * (so, in this case, clearNodeScope will be called before the popNode).
	 */
	@Override
	public SimpleNode popNode()
	{
		if (--sp < mk)
		{
			clearMark();
		}
		return nodes.pop();
	}

	/* Returns the node currently on the top of the stack. */
	@Override
	public SimpleNode peekNode()
	{
		return nodes.peek();
	}

	/* Returns the node currently on the top of the stack. */
	@Override
	public SimpleNode peekNode(int i)
	{
		return nodes.peek(i);
	}

	/*
	 * Returns the number of children on the stack in the current node scope.
	 */
	@Override
	public int nodeArity()
	{
		return sp - mk;
	}

	/**
	 * Called when some exception is raised after the open (so, the proper close
	 * won't be called). E.g.: the with construct will end up calling a clear as
	 * it's based on a treated exception in the python 2.5 grammar.
	 * 
	 * Note that the popNode may still be called after this method.
	 */
	@Override
	public void clearNodeScope(Node n)
	{
		while (sp > mk)
		{
			popNode();
		}
		lines.pop();
		columns.pop();

		clearMark();
	}

	/**
	 * Open a new scope (which may result in a new SimpleNode if the close is
	 * properly called later on).
	 */
	@Override
	public void openNodeScope(Node n)
	{
		Token t = this.grammar.getToken(1);
		lines.push(t.beginLine);
		columns.push(t.beginColumn);

		marks.push(mk);
		mk = sp;
	}

	/*
	 * A definite node is constructed from a specified number of children. That
	 * number of nodes are popped from the stack and made the children of the
	 * definite node. Then the definite node is pushed on to the stack.
	 */
	@Override
	public void closeNodeScope(final Node n, int num) throws ParseException
	{
		int line = lines.pop();
		int col = columns.pop();
		SimpleNode sn = (SimpleNode) n;
		clearMark();
		SimpleNode newNode = null;
		try
		{
			newNode = builder.closeNode(sn, num);
			if (ITreeBuilder.DEBUG_TREE_BUILDER)
			{
				System.out.println("Created node: " + newNode);
			}
		}
		catch (ParseException exc)
		{
			throw exc;
		}
		catch (Exception exc)
		{
			throw new ParseException("Internal error:" + exc);
		}
		if (newNode == null) { throw new ParseException("Internal AST builder error"); }

		pushNode(n, newNode, line, col);
		node_created = true;
	}

	/*
	 * A conditional node is constructed if its condition is true. All the nodes
	 * that have been pushed since the node was opened are made children of the
	 * the conditional node, which is then pushed on to the stack. If the
	 * condition is false the node is not constructed and they are left on the
	 * stack.
	 */
	@Override
	public void closeNodeScope(final Node n, boolean condition) throws ParseException
	{
		int line = lines.pop();
		int col = columns.pop();
		SimpleNode sn = (SimpleNode) n;
		if (condition)
		{
			SimpleNode newNode = null;
			try
			{
				newNode = builder.closeNode(sn, nodeArity());
				if (ITreeBuilder.DEBUG_TREE_BUILDER)
				{
					System.out.println("Created node: " + newNode);
				}
			}
			catch (ParseException exc)
			{
				throw exc;

			}
			catch (ClassCastException exc)
			{
				throw new ParseException("Internal error:" + exc, sn);

			}
			catch (Exception exc)
			{
				throw new ParseException("Internal error:" + exc, sn);
			}
			if (newNode == null) { throw new ParseException("Internal AST builder error when closing node:" + sn); }
			clearMark();

			pushNode(n, newNode, line, col);
			node_created = true;
		}
		else
		{
			clearMark();
			node_created = false;
		}
	}

	private void clearMark()
	{
		if (marks.size() > 0)
		{
			mk = marks.pop();
		}
		else
		{
			mk = 0;
		}
	}

}

/**
 * IntStack implementation. During all the tests, it didn't have it's size
 * raised, so, 50 is probably a good overall size... (max on python lib was 40)
 */
final class IntStack
{
	int[]	stack;
	int	  sp	= 0;

	public IntStack()
	{
		stack = new int[50];
	}

	public void removeAllElements()
	{
		sp = 0;
	}

	public int size()
	{
		return sp;
	}

	public int elementAt(int idx)
	{
		return stack[idx];
	}

	public void push(int val)
	{
		if (sp >= stack.length)
		{
			int[] newstack = new int[sp * 2];
			System.arraycopy(stack, 0, newstack, 0, sp);
			stack = newstack;
		}
		stack[sp++] = val;
	}

	public int pop()
	{
		return stack[--sp];
	}
}
