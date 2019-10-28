///////////////////////////////////////////////////////////////////////////////
//
// PACKAGE   : com.astra.ses.spell.gui.model.commands
// 
// FILE      : ShowReleaseInfo.java
//
// DATE      : 2008-11-21 08:55
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
// SUBPROJECT: SPELL GUI Client
//
///////////////////////////////////////////////////////////////////////////////
package com.astra.ses.spell.gui.model.commands;

import java.io.File;
import java.io.IOException;
import java.io.InputStream;
import java.net.URL;
import java.net.URLConnection;

import org.eclipse.core.commands.AbstractHandler;
import org.eclipse.core.commands.ExecutionEvent;
import org.eclipse.core.commands.ExecutionException;
import org.eclipse.jface.dialogs.MessageDialog;
import org.eclipse.ui.IWorkbenchWindow;
import org.eclipse.ui.PlatformUI;
import org.eclipse.ui.internal.UIPlugin;

import com.astra.ses.spell.gui.Activator;
import com.astra.ses.spell.gui.core.interfaces.ServiceManager;
import com.astra.ses.spell.gui.core.model.server.ContextInfo;
import com.astra.ses.spell.gui.core.model.server.ServerInfo;
import com.astra.ses.spell.gui.dialogs.ReleaseInfoDialog;
import com.astra.ses.spell.gui.services.IRuntimeSettings;
import com.astra.ses.spell.gui.services.IRuntimeSettings.RuntimeProperty;

/*******************************************************************************
 * @brief Command for showing the release information
 * @date 09/10/07
 ******************************************************************************/
public class ShowGUIReleaseInfo extends AbstractHandler
{
	public static final String	ID	= "com.astra.ses.spell.gui.commands.ShowGUIReleaseInfo";

	// =========================================================================
	// # INSTANCE DATA MEMBERS
	// =========================================================================

	// PRIVATE -----------------------------------------------------------------

	// PROTECTED ---------------------------------------------------------------
	// PUBLIC ------------------------------------------------------------------

	// =========================================================================
	// # ACCESIBLE METHODS
	// =========================================================================

	public CommandResult execute(ExecutionEvent event)
	        throws ExecutionException
	{
		// Search the release information file
		URL entry = Activator.getDefault().getBundle().getEntry("RELEASENOTES");
		
		IWorkbenchWindow window = PlatformUI.getWorkbench()
		        .getActiveWorkbenchWindow();
		String path = "";
		// Try to find file in different cases
		IRuntimeSettings runtime = (IRuntimeSettings) ServiceManager.get(IRuntimeSettings.class);
		ServerInfo info = (ServerInfo) runtime.getRuntimeProperty(RuntimeProperty.ID_SERVER_SELECTION);
		
	
		try {
			InputStream in = entry.openStream();
			StringBuilder builder = new StringBuilder();
			byte[] buffer = new byte[4096];
			for (int length = 0;(length = in.read(buffer)) > 0;){
				builder.append(new String(buffer,0,length,"UTF-8"));
			}
			in.close();
			ReleaseInfoDialog dialog = new ReleaseInfoDialog(window.getShell(),
					builder.toString());
			dialog.open();
			return CommandResult.SUCCESS;
		} catch (IOException e) {
			MessageDialog.openWarning(window.getShell(), "Release Information",
			        "No release information available\n'" + path + "'\n" + e);
			return CommandResult.NO_EFFECT;
		}
	}

}
