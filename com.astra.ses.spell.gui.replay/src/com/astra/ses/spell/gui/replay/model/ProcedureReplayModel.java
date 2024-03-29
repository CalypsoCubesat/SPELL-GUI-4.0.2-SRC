///////////////////////////////////////////////////////////////////////////////
//
// PACKAGE   : com.astra.ses.spell.gui.replay.model
// 
// FILE      : ProcedureReplayModel.java
//
// DATE      : Jun 19, 2013
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
package com.astra.ses.spell.gui.replay.model;

import java.util.Map;

import org.eclipse.core.runtime.IProgressMonitor;

import com.astra.ses.spell.gui.core.interfaces.IFileManager;
import com.astra.ses.spell.gui.core.interfaces.ServiceManager;
import com.astra.ses.spell.gui.core.model.types.ClientMode;
import com.astra.ses.spell.gui.core.model.types.Level;
import com.astra.ses.spell.gui.core.model.types.ProcProperties;
import com.astra.ses.spell.gui.core.utils.Logger;
import com.astra.ses.spell.gui.procs.interfaces.model.AsRunReplayResult;
import com.astra.ses.spell.gui.procs.interfaces.model.IProcedureController;
import com.astra.ses.spell.gui.procs.model.Procedure;
import com.astra.ses.spell.gui.procs.services.ExecutionPlayer;

public class ProcedureReplayModel extends Procedure
{
	private String m_asrunPath;
	private ExecutionPlayer m_player;
	
	private static IFileManager s_fmgr = null;
	
	/***************************************************************************
	 * 
	 **************************************************************************/
	public ProcedureReplayModel( String instanceId, Map<ProcProperties,String> properties )
	{
		super(instanceId, properties, ClientMode.UNKNOWN);
		
		if (s_fmgr == null)
		{
			s_fmgr = (IFileManager) ServiceManager.get(IFileManager.class);
		}
		
	}
	
	/***************************************************************************
	 * 
	 **************************************************************************/
	@Override
	protected IProcedureController createProcedureController()
	{
		return new ProcedureReplayController(this);
	}
	
	/***************************************************************************
	 * 
	 **************************************************************************/
	public void load( String asrunPath, IProgressMonitor monitor ) throws Exception
	{
		Logger.info("Replaying ASRUN", Level.PROC, this);
		getExecutionManager().initialize(monitor);
		getExecutionManager().setRunInto(true);
		getController().refresh();
		Logger.info("Remote ASRUN path is " + asrunPath, Level.PROC, this);
		m_asrunPath = asrunPath;
		IFileManager fileMgr = (IFileManager) ServiceManager.get(IFileManager.class);
		String localAsRunPath = fileMgr.downloadServerFile(m_asrunPath, monitor);
		Logger.info("Creating execution player", Level.PROC, this);
        m_player = new ExecutionPlayer(this,localAsRunPath,null);
		setReplayMode(true);
		AsRunReplayResult result = new AsRunReplayResult();
		Logger.info("Starting replay...", Level.PROC, this);
		m_player.replay(monitor, 0,result);
		Logger.info("Replay result: " + result.status, Level.PROC, this);
		setReplayMode(false);
	}
}
