///////////////////////////////////////////////////////////////////////////////
//
// PACKAGE   : com.astra.ses.spell.language.common
// 
// FILE      : Reflection.java
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

import java.lang.reflect.Field;
import java.lang.reflect.Method;
import java.lang.reflect.Modifier;

public class Reflection {

    /**
     * @return true if the passed object has a field with the name passed.
     */
    public static boolean hasAttr(Object o, String attr) {
        try {
            o.getClass().getDeclaredField(attr);
        } catch (SecurityException e) {
            return false;
        } catch (NoSuchFieldException e) {
            return false;
        }
        return true;
    }

    /**
     * @return the field from a class that matches the passed attr name (or null if it couldn't be found)
     */
    public static Field getAttrFromClass(Class<? extends Object> c, String attr) {
        try {
            return c.getDeclaredField(attr);
        } catch (SecurityException e) {
        } catch (NoSuchFieldException e) {
        }
        return null;
    }

    /**
     * @return the field from a class that matches the passed attr name (or null if it couldn't be found)
     * @see Reflection#getAttrObj(Object, String) to get the actual value of the field.
     */
    public static Field getAttr(Object o, String attr) {
        try {
            return o.getClass().getDeclaredField(attr);
        } catch (Exception e) {
        }
        return null;
    }

    public static Field getAttr(Object o, String attr, boolean raiseExceptionIfNotAvailable) {
        try {
            return o.getClass().getDeclaredField(attr);
        } catch (Exception e) {
            if (raiseExceptionIfNotAvailable) {
                throw new RuntimeException("Unable to get field: " + attr + " in: " + o.getClass(), e);
            }
            return null;
        }
    }

    public static Object getAttrObj(Object o, String attr) {
        return Reflection.getAttrObj(o, attr, false);
    }

    public static Object getAttrObj(Object o, String attr, boolean raiseExceptionIfNotAvailable) {
        return Reflection.getAttrObj(o.getClass(), o, attr, raiseExceptionIfNotAvailable);
    }

    /**
     * @return the value of some attribute in the given object
     */
    public static Object getAttrObj(Class<? extends Object> c, Object o, String attr,
            boolean raiseExceptionIfNotAvailable) {
        try {
            Field field = getAttrFromClass(c, attr);
            if (field != null) {
                //get it even if it's not public!
                if ((field.getModifiers() & Modifier.PUBLIC) == 0) {
                    field.setAccessible(true);
                }
                Object obj = field.get(o);
                return obj;
            }
        } catch (Exception e) {
            //ignore
            if (raiseExceptionIfNotAvailable) {
                throw new RuntimeException(e);
            }
        }
        return null;
    }

    /**
     * Calls a method for an object
     * 
     * @param obj the object with the method we want to call
     * @param name the method name
     * @param args the arguments received for the call
     * @return the return of the method
     * 
     * @throws RuntimeException if the object could not be invoked
     */
    public static Object invoke(Object obj, String name, Object... args) {
        //the args are not checked for the class because if a subclass is passed, the method is not correctly gotten
        //another method might do it...
        Method m = Reflection.findMethod(obj, name, args);
        return Reflection.invoke(obj, m, args);
    }

    /**
     * @see invoke
     */
    public static Object invoke(Object obj, Method m, Object... args) {
        try {
            return m.invoke(obj, args);
        } catch (Exception e) {
            throw new RuntimeException(e);
        }
    }

    /**
     * @return a method that has the given name and arguments
     * @throws RuntimeException if the method could not be found
     */
    public static Method findMethod(Object obj, String name, Object... args) {
        return Reflection.findMethod(obj.getClass(), name, args);
    }

    /**
     * @return a method that has the given name and arguments
     * @throws RuntimeException if the method could not be found
     */
    public static Method findMethod(Class<? extends Object> class_, String name, Object... args) {
        try {
            Method[] methods = class_.getMethods();
            for (Method method : methods) {

                Class<? extends Object>[] parameterTypes = method.getParameterTypes();
                if (method.getName().equals(name) && parameterTypes.length == args.length) {
                    //check the parameters
                    int i = 0;
                    for (Class<? extends Object> param : parameterTypes) {
                        if (!param.isInstance(args[i])) {
                            continue;
                        }
                        i++;
                    }
                    //invoke it
                    return method;
                }
            }
        } catch (Exception e) {
            throw new RuntimeException(e);
        }
        throw new RuntimeException("The method with name: " + name
                + " was not found (or maybe it was found but the parameters didn't match).");
    }

}
