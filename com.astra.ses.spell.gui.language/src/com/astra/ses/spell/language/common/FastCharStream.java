///////////////////////////////////////////////////////////////////////////////
//
// PACKAGE   : com.astra.ses.spell.language.common
// 
// FILE      : FastCharStream.java
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

import com.astra.ses.spell.language.model.ObjectsPool.ObjectsPoolMap;
import com.astra.ses.spell.language.model.Token;

/**
 * An implementation of interface CharStream, where the data is read from a
 * Reader. Completely recreated so that we can read data directly from a String,
 * as the initial implementation was highly inefficient when working only with a
 * string (actually, if it was small, there would be no noticeable delays, but
 * if it became big, then the improvement would be HUGE).
 * 
 * It keeps the same semantics for line and column stuff (and shares the
 * previous approach of keeping a buffer for this info). If we wanted we could
 * optimize it for also taking less memory, but as there is usually not so many
 * concurrent parses, this is probably not worth it -- and it would probably be
 * a little slower)
 */

public final class FastCharStream
{

	public final char[]	         buffer;

	public final int	         bufline[];

	public final int	         bufcolumn[];

	private boolean	             prevCharIsCR	= false;

	private boolean	             prevCharIsLF	= false;

	private int	                 column	      = 0;

	private int	                 line	      = 1;

	public int	                 bufpos	      = -1;

	private int	                 updatePos;

	public int	                 tokenBegin;

	private static IOException	 ioException;

	private static final boolean	DEBUG	  = false;

	public FastCharStream(char cs[])
	{
		this.buffer = cs;
		this.bufline = new int[cs.length];
		this.bufcolumn = new int[cs.length];
	}

	public int getCurrentPos()
	{
		return bufpos;
	}

	public void restorePos(int pos)
	{
		bufpos = pos;
	}

	/**
	 * Restores a previous position. Don't forget to restore the level if eof
	 * was already found!
	 */
	public void restoreLineColPos(final int endLine, final int endColumn)
	{
		final int initialBufPos = bufpos;
		final int currLine = getEndLine();

		if (currLine < endLine)
		{
			return;
		}
		else if (currLine == endLine && getEndColumn() < endColumn)
		{
			return;
		}

		while ((getEndLine() != endLine || getEndColumn() != endColumn) && bufpos >= 0)
		{
			bufpos--;
		}

		if (bufpos < 0 || getEndLine() != endLine)
		{
			// we couldn't find it. Let's restore the position when we started
			// it.
			bufpos = initialBufPos;
		}
	}

	public final char readChar() throws IOException
	{
		try
		{
			bufpos++;
			char r = this.buffer[bufpos];

			if (bufpos >= updatePos)
			{
				updatePos++;

				// start UpdateLineCol
				column++;

				if (prevCharIsLF)
				{
					prevCharIsLF = false;
					line += (column = 1);

				}
				else if (prevCharIsCR)
				{

					prevCharIsCR = false;
					if (r == '\n')
					{
						prevCharIsLF = true;
					}
					else
					{
						line += (column = 1);
					}
				}

				if (r == '\r')
				{
					prevCharIsCR = true;

				}
				else if (r == '\n')
				{
					prevCharIsLF = true;

				}

				bufline[bufpos] = line;
				bufcolumn[bufpos] = column;
				// end UpdateLineCol
			}

			return r;
		}
		catch (ArrayIndexOutOfBoundsException e)
		{
			bufpos--;
			if (ioException == null)
			{
				ioException = new IOException();
			}
			throw ioException;
		}
	}

	public final int getEndColumn()
	{
		return bufcolumn[bufpos];
	}

	public final int getEndLine()
	{
		return bufline[bufpos];
	}

	public final int getBeginColumn()
	{
		return bufcolumn[tokenBegin];
	}

	public final int getBeginLine()
	{
		return bufline[tokenBegin];
	}

	public final void backup(int amount)
	{
		if (DEBUG)
		{
			System.out.println("FastCharStream: backup >>" + amount + "<<");
		}
		bufpos -= amount;
	}

	public final char BeginToken() throws IOException
	{
		char c = readChar();
		tokenBegin = bufpos;
		if (DEBUG)
		{
			System.out.println("FastCharStream: BeginToken >>" + (int) c + "<<");
		}
		return c;
	}

	private final ObjectsPoolMap	interned	= new ObjectsPoolMap();

	public final String GetImage()
	{
		String string;
		if (bufpos >= tokenBegin)
		{
			string = new String(buffer, tokenBegin, bufpos - tokenBegin + 1);
		}
		else
		{
			string = new String(buffer, tokenBegin, buffer.length - tokenBegin + 1);
		}

		String existing = interned.get(string);
		if (existing != null) { return existing; }
		interned.put(string, string);
		return string;
	}

	public final void AppendSuffix(FastStringBuffer buf, int len)
	{
		if (len > 0)
		{
			try
			{
				int initial = bufpos - len + 1;
				if (initial < 0)
				{
					int initial0 = initial;
					len += initial;
					initial = 0;
					buf.appendN('\u0000', -initial0);
					buf.append(buffer, initial, len);
				}
				else
				{
					buf.append(buffer, initial, len);
				}
			}
			catch (Exception e)
			{
				e.printStackTrace();
			}
		}
	}

	public static boolean	ACCEPT_GET_SUFFIX	= false;

	public final char[] GetSuffix(int len)
	{
		if (!ACCEPT_GET_SUFFIX) { throw new RuntimeException("This method should not be used (AppendSuffix should be used instead)."); }
		char[] ret = new char[len];
		if (len > 0)
		{
			try
			{
				int initial = bufpos - len + 1;
				if (initial < 0)
				{
					int initial0 = initial;
					len += initial;
					initial = 0;
					System.arraycopy(buffer, initial, ret, -initial0, len);
				}
				else
				{
					System.arraycopy(buffer, initial, ret, 0, len);
				}
			}
			catch (Exception e)
			{
				e.printStackTrace();
			}
		}
		if (DEBUG)
		{
			System.out.println("FastCharStream: GetSuffix:" + len + " >>" + new String(ret) + "<<");
		}
		return ret;
	}

	public void setBeginEndCharsEqual(Token t)
	{
		t.beginLine = t.endLine = bufline[tokenBegin];
		t.beginColumn = t.endColumn = bufcolumn[tokenBegin];
	}

	public void setBeginEndChars(Token t)
	{
		t.beginLine = bufline[tokenBegin];
		t.beginColumn = bufcolumn[tokenBegin];
		t.endLine = bufline[bufpos];
		t.endColumn = bufcolumn[bufpos];
	}

}
