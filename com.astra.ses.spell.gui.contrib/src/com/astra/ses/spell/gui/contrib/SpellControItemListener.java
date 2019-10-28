package com.astra.ses.spell.gui.contrib;

import java.util.Arrays;
import java.util.List;

import com.astra.ses.spell.gui.core.model.notification.ItemNotification;
import com.astra.ses.spell.gui.core.model.types.ExecutionMode;
import com.astra.ses.spell.gui.core.model.types.ItemType;
import com.astra.ses.spell.gui.interfaces.listeners.IGuiProcedureItemsListener;
import com.astra.ses.spell.gui.procs.interfaces.model.IProcedure;

public class SpellControItemListener implements IGuiProcedureItemsListener {

	@Override
	public String getListenerId() {
		// TODO Auto-generated method stub
		return "SPELL Control Contribution";
	}
	
	@Override
	public void notifyItem(IProcedure model, ItemNotification data) {
		if (!data.getExecutionMode().equals(ExecutionMode.REPLAY) && data.getType().equals(ItemType.SYSTEM)){
			// This gives the list of item names: 
			String actionName = data.getItemName().get(0);
			String contribType = data.getItemValue().get(0);
			List<String> contribData = Arrays.asList(data.getItemStatus().get(0).split("\\|"));
			if (actionName.toUpperCase().equals("CREATE")){
				SpellControlContribution.get().addContribution(contribType, contribData);
			} else if (actionName.toUpperCase().equals("UPDATE")){
				SpellControlContribution.get().updateContribution(contribType, contribData);
			} else if (actionName.toUpperCase().equals("DELETE")){
				SpellControlContribution.get().deleteContribution(contribType);
			}
		}
	}

}
