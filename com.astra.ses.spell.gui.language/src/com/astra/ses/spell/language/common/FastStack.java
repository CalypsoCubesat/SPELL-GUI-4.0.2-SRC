///////////////////////////////////////////////////////////////////////////////
//
// PACKAGE   : com.astra.ses.spell.language.common
// 
// FILE      : FastStack.java
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

import java.util.EmptyStackException;
import java.util.Iterator;
import java.util.ListIterator;
import java.util.NoSuchElementException;

/**
 * Note: not thread-safe!
 * 
 * Note: Doesn't release items not used for garbage collection until a new item
 * is added at that place
 * 
 * @author Fabio
 * 
 * @param <E>
 */
public final class FastStack<E> implements Iterable<E>
{

	private E[]	elementData;

	private int	size;	     // = 0

	/**
	 * Creates an empty Stack.
	 */
	@SuppressWarnings("unchecked")
	public FastStack(int initialCapacity)
	{
		this.elementData = (E[]) new Object[initialCapacity];
	}

	/**
	 * Pushes an item onto the top of this stack.
	 * 
	 * @param item
	 *            the item to be pushed onto this stack.
	 * @return the <code>item</code> argument.
	 */
	public E push(E item)
	{
		if (elementData.length < size + 1)
		{
			ensureCapacity(size + 1);
		}
		this.elementData[size] = item;
		size++;
		return item;
	}

	/**
	 * Removes the object at the top of this stack and returns that object as
	 * the value of this function.
	 * 
	 * @return The object at the top of this stack
	 * @exception EmptyStackException
	 *                if this stack is empty.
	 */
	public E pop()
	{
		if (size == 0) { throw new EmptyStackException(); }
		size--;
		E item = this.elementData[size];
		this.elementData[size] = null; // make it available for garbage
									   // collection
		return item;
	}

	/**
	 * Looks at the object at the top of this stack without removing it from the
	 * stack.
	 * 
	 * @return the object at the top of this stack.
	 * @exception EmptyStackException
	 *                if this stack is empty.
	 */
	public E peek()
	{
		if (size == 0) { throw new EmptyStackException(); }
		return this.elementData[size - 1];
	}

	/**
	 * Tests if this stack is empty.
	 * 
	 * @return <code>true</code> if and only if this stack contains no items;
	 *         <code>false</code> otherwise.
	 */
	public boolean empty()
	{
		return size == 0;
	}

	public Iterator<E> topDownIterator()
	{
		final ListIterator<E> l = new ListItr(this.size);
		return new Iterator<E>()
		{

			public boolean hasNext()
			{
				return l.hasPrevious();
			}

			public E next()
			{
				return l.previous();
			}

			public void remove()
			{
				throw new RuntimeException("Not Impl");
			}

		};
	}

	public int size()
	{
		return size;
	}

	public ListIterator<E> iterator()
	{
		return new ListItr(0);
	}

	public E get(int i)
	{
		if (i >= size) { throw new ArrayIndexOutOfBoundsException(); }
		return elementData[i];
	}

	public void addAll(FastStack<? extends E> items)
	{
		ensureCapacity(size + items.size);
		System.arraycopy(items.elementData, 0, this.elementData, size, items.size);
		size = size + items.size;
	}

	@SuppressWarnings("unchecked")
	private void ensureCapacity(int minCapacity)
	{
		int oldCapacity = elementData.length;
		if (minCapacity > oldCapacity)
		{
			Object oldData[] = elementData;
			int newCapacity = (oldCapacity * 3) / 2 + 1;
			if (newCapacity < minCapacity)
			{
				newCapacity = minCapacity;
			}
			elementData = (E[]) new Object[newCapacity];
			System.arraycopy(oldData, 0, elementData, 0, size);
		}
	}

	public E getFirst()
	{
		return this.elementData[0];
	}

	public FastStack<E> createCopy()
	{
		FastStack<E> ret = new FastStack<E>(size + 15);
		System.arraycopy(this.elementData, 0, ret.elementData, 0, size);
		ret.size = size;
		return ret;
	}

	public void clear()
	{
		size = 0;
	}

	public void removeAllElements()
	{
		size = 0;
	}

	public boolean isEmpty()
	{
		return size == 0;
	}

	private class ListItr implements ListIterator<E>
	{

		/**
		 * Index of element to be returned by subsequent call to next.
		 */
		int	cursor	= 0;

		public boolean hasNext()
		{
			return cursor != size();
		}

		public E next()
		{
			try
			{
				E next = get(cursor);
				return next;
			}
			catch (IndexOutOfBoundsException e)
			{
				throw new NoSuchElementException();
			}
		}

		public void remove()
		{
			throw new RuntimeException("Not implemented");
		}

		public void add(E o)
		{
			throw new RuntimeException("Not implemented");
		}

		ListItr(int index)
		{
			cursor = index;
		}

		public boolean hasPrevious()
		{
			return cursor != 0;
		}

		public E previous()
		{
			try
			{
				int i = cursor - 1;
				E previous = get(i);
				return previous;
			}
			catch (IndexOutOfBoundsException e)
			{
				throw new NoSuchElementException();
			}
		}

		public int nextIndex()
		{
			return cursor;
		}

		public int previousIndex()
		{
			return cursor - 1;
		}

		public void set(E o)
		{
			throw new RuntimeException("Not implemented");
		}
	}

	@Override
	public String toString()
	{
		FastStringBuffer buf = new FastStringBuffer("FastStack [\n", 25 * this.size);
		for (E element : this)
		{
			buf.append("    ");
			buf.append(element.toString());
			buf.append("\n");
		}
		buf.append("]");
		return buf.toString();
	}

	public int hashCode()
	{
		throw new RuntimeException("Not hashable");
	}

	public boolean equals(Object o)
	{
		throw new RuntimeException("Not comparable");
	}

	/**
	 * Peeks an element from the list with an index used from top to bottom
	 * 
	 * @param i
	 *            if 0, it's the same as peek(), otherwise, it'll go and peek
	 *            items at other levels depending on this index E.g.: i == 1
	 *            will peek one level below i == 0.
	 * 
	 * @return the peeked element
	 */
	public E peek(int i)
	{
		return this.elementData[size - 1 - i];
	}

}
