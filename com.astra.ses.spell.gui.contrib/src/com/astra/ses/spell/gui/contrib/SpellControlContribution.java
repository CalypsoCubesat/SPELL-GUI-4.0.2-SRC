///////////////////////////////////////////////////////////////////////////////
//
// Copyright (C) 2013 GMV S.A.U.
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
///////////////////////////////////////////////////////////////////////////////
package com.astra.ses.spell.gui.contrib;

import java.util.Hashtable;
import java.util.LinkedHashMap;
import java.util.List;

import org.eclipse.jface.action.ContributionItem;
import org.eclipse.swt.SWT;
import org.eclipse.swt.graphics.Point;
import org.eclipse.swt.graphics.Rectangle;
import org.eclipse.swt.layout.GridLayout;
import org.eclipse.swt.widgets.Composite;
import org.eclipse.swt.widgets.CoolBar;
import org.eclipse.swt.widgets.Menu;
import org.eclipse.swt.widgets.ToolBar;
import org.eclipse.ui.menus.IWorkbenchContribution;
import org.eclipse.ui.menus.WorkbenchWindowControlContribution;
import org.eclipse.ui.services.IServiceLocator;

import com.astra.ses.spell.gui.core.interfaces.ServiceManager;
import com.astra.ses.spell.gui.preferences.interfaces.IConfigurationManager;

/**
 * This class provides a clock control that can be put in a toolbar.
 */
public class SpellControlContribution extends WorkbenchWindowControlContribution implements IWorkbenchContribution {
	
	private static SpellControlContribution instance = null;
	private static IConfigurationManager s_cfg = (IConfigurationManager) ServiceManager.get(IConfigurationManager.class);
	
	public static SpellControlContribution get() {
		return instance;
	}

	private static LinkedHashMap<String,SpellGUIContributionItem> spellGUIContributions = new LinkedHashMap<String,SpellGUIContributionItem>();

	private Composite contributionBase;
	
	protected Composite createControl(Composite parent)
	{
		instance = this;
		contributionBase = new Composite(parent, SWT.NULL); 

        GridLayout layout = new GridLayout();
        layout.marginTop = 0;
        layout.marginHeight = 0;
        layout.marginWidth = 0;
        layout.marginLeft = 5;
        layout.marginRight = 0;
        layout.marginBottom = 0;
        layout.numColumns = 5;
        contributionBase.setLayout( layout );
        
        for (SpellGUIContributionItem contribution : spellGUIContributions.values()) {
        	if (contribution.getRoot() != null && ! contribution.getRoot().isDisposed())
        		contribution.getRoot().dispose();
        	contribution.createContent(contributionBase);
        	contribution.update();
		}
        update();

        return contributionBase;
	}
	
	/* (non-Javadoc)
	 * @see org.eclipse.jface.action.ContributionItem#dispose()
	 */
	@Override
	public void dispose()
	{
		for (SpellGUIContributionItem contrib : spellGUIContributions.values()) {
			contrib.dispose();
		}
		super.dispose();
	}	
	
	
	@Override
	public boolean isDirty() {
		return true;
	}
	
	@Override
	public boolean isDynamic() {
		return true;
	}
	
	@Override
	public void update() {

		Point computeSize = contributionBase.computeSize(SWT.DEFAULT, SWT.DEFAULT);
		Rectangle bounds = contributionBase.getParent().getParent().getBounds();
		bounds.height = computeSize.y;
		bounds.width = computeSize.x+15;
		//bounds.x = 0;
		//bounds.y = 0;
		contributionBase.getParent().getParent().setBounds(bounds);

		contributionBase.getParent().getParent().getParent().getParent().layout();
		
		contributionBase.getParent().pack();
	}
	
	public void addContribution(String type,List<String> data){
		SpellGUIContributionItem contribution = spellGUIContributions.get(type);
		if (contribution == null){
			contribution = SpellGUIContributionItemFactory.createContribution(type);
			spellGUIContributions.put(type, contribution);
			contribution.setData(data);
			contribution.createContent(contributionBase);
			contribution.update();
		} else {
			contribution.setData(data);
			contribution.update();	
		}
		update();
		
	}
	
	public void updateContribution(String type,List<String> data){
		SpellGUIContributionItem contribution = spellGUIContributions.get(type);
		if (contribution == null){
			return;
		}
		
		contribution.setData(data);
		contribution.update();
		
		update();
	}
	
	public void deleteContribution(String type){
		SpellGUIContributionItem contribution = spellGUIContributions.get(type);
		if (contribution != null){
			contribution.dispose();
			spellGUIContributions.remove(type);
		}
		
		update();
	}

	@Override
	public void initialize(IServiceLocator serviceLocator) {
		
	}
	
}

