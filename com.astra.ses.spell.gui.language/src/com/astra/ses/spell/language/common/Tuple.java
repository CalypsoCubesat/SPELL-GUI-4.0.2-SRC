///////////////////////////////////////////////////////////////////////////////
//
// PACKAGE   : com.astra.ses.spell.language.common
// 
// FILE      : Tuple.java
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
/*
 * Created on 24/09/2005
 */
package com.astra.ses.spell.language.common;

import java.io.Serializable;

/**
 * Defines a tuple of some object, adding equals and hashCode operations
 * 
 * @author Fabio
 */
public final class Tuple<X, Y> implements Serializable
{

	private static final long	serialVersionUID	= 1L;

	public X	              o1;
	public Y	              o2;

	public Tuple(X o1, Y o2)
	{
		this.o1 = o1;
		this.o2 = o2;
	}

	@SuppressWarnings("rawtypes")
	@Override
	public boolean equals(Object obj)
	{
		if (!(obj instanceof Tuple)) { return false; }

		Tuple t2 = (Tuple) obj;
		if (o1 == t2.o1 && o2 == t2.o2)
		{ // all the same
			return true;
		}

		if (o1 == null && t2.o1 != null) { return false; }
		if (o2 == null && t2.o2 != null) { return false; }
		if (o1 != null && t2.o1 == null) { return false; }
		if (o2 != null && t2.o2 == null) { return false; }

		if (!o1.equals(t2.o1)) { return false; }
		if (!o2.equals(t2.o2)) { return false; }
		return true;
	}

	@Override
	public int hashCode()
	{
		if (o1 != null && o2 != null) { return o1.hashCode() * o2.hashCode(); }
		if (o1 != null) { return o1.hashCode(); }
		if (o2 != null) { return o2.hashCode(); }
		return 7;
	}

	@Override
	public String toString()
	{
		FastStringBuffer buffer = new FastStringBuffer();
		buffer.append("Tuple [");
		buffer.appendObject(o1);
		buffer.append(" -- ");
		buffer.appendObject(o2);
		buffer.append("]");
		return buffer.toString();
	}
}
