///////////////////////////////////////////////////////////////////////////////
//
// PACKAGE   : com.astra.ses.spell.gui.core.comm.socket.utils
// 
// FILE      : Authenticator.java
//
// DATE      : Aug 2, 2013
//
// Copyright (C) 2008, 2015 SES ENGINEERING, Luxembourg S.A.R.L.
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
///////////////////////////////////////////////////////////////////////////////
package com.astra.ses.spell.gui.core.comm.socket.utils;

import java.io.File;
import java.io.IOException;

import com.astra.ses.spell.gui.core.model.server.AuthenticationData;
import com.astra.ses.spell.gui.core.model.types.Level;
import com.astra.ses.spell.gui.core.utils.Logger;
import com.trilead.ssh2.Connection;
import com.trilead.ssh2.InteractiveCallback;

public class Authenticator
{
	public static boolean authenticate( Connection connection, final AuthenticationData auth ) throws IOException
	{
		boolean isAuthenticated = false;
		if (auth.getMode().equals(AuthenticationData.Mode.KEY))
		{
			Logger.info("Authenticating with key file: '" + auth.getKeyFile() + "'", Level.COMM, Authenticator.class);
			File rsa = new File(auth.getKeyFile());
			if (rsa.exists() && rsa.canRead())
			{
				isAuthenticated = connection.authenticateWithPublicKey(auth.getUsername(), rsa , "");
			}
			else
			{
				Logger.warning("Cannot read RSA/DSA key: '" + auth.getKeyFile() + "'", Level.COMM, Authenticator.class);
			}
			if (!isAuthenticated && auth.getPassword()!=null)
			{
				Logger.warning("Falling back to password authentication", Level.COMM, Authenticator.class);
				if (connection.isAuthMethodAvailable(auth.getUsername(), "password")){
					isAuthenticated = connection.authenticateWithPassword( auth.getUsername(), auth.getPassword() );
				} else {
					isAuthenticated = connection.authenticateWithKeyboardInteractive( auth.getUsername(), new InteractiveCallback(){
						@Override
						public String[] replyToChallenge(String arg0, String arg1, int arg2, String[] arg3,
								boolean[] arg4) throws Exception {
							if (arg3.length == 0)
								return arg3;
							return  new String[]{auth.getPassword()};
						}
					});
				}
				
			}
		}
		else
		{
			Logger.warning("Authenticating with password", Level.COMM, Authenticator.class);
			if (connection.isAuthMethodAvailable(auth.getUsername(), "password")){
				isAuthenticated = connection.authenticateWithPassword( auth.getUsername(), auth.getPassword() );
			} else {
				isAuthenticated = connection.authenticateWithKeyboardInteractive( auth.getUsername(), new InteractiveCallback(){
					@Override
					public String[] replyToChallenge(String arg0, String arg1, int arg2, String[] arg3,
							boolean[] arg4) throws Exception {
						if (arg3.length == 0)
							return arg3;
						return  new String[]{auth.getPassword()};
					}
				});
			}
		}
		
		if (isAuthenticated == false) throw new IOException("Authentication failed.");
		return isAuthenticated;
	}
}
