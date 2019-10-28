// Autogenerated AST node
package com.astra.ses.spell.language.model.ast;

public final class NameTok extends NameTokType implements name_contextType
{
	public String	id;
	public int	  ctx;

	public NameTok(String id, int ctx)
	{
		this.id = id;
		this.ctx = ctx;
	}

	public int hashCode()
	{
		final int prime = 31;
		int result = 1;
		result = prime * result + ((id == null) ? 0 : id.hashCode());
		result = prime * result + ctx;
		return result;
	}

	public boolean equals(Object obj)
	{
		if (this == obj) return true;
		if (obj == null) return false;
		if (getClass() != obj.getClass()) return false;
		NameTok other = (NameTok) obj;
		if (id == null)
		{
			if (other.id != null) return false;
		}
		else if (!id.equals(other.id)) return false;
		if (this.ctx != other.ctx) return false;
		return true;
	}

	public NameTok createCopy()
	{
		return createCopy(true);
	}

	public NameTok createCopy(boolean copyComments)
	{
		NameTok temp = new NameTok(id, ctx);
		temp.beginLine = this.beginLine;
		temp.beginColumn = this.beginColumn;
		if (this.specialsBefore != null && copyComments)
		{
			for (Object o : this.specialsBefore)
			{
				if (o instanceof commentType)
				{
					commentType commentType = (commentType) o;
					temp.getSpecialsBefore().add(commentType.createCopy(copyComments));
				}
			}
		}
		if (this.specialsAfter != null && copyComments)
		{
			for (Object o : this.specialsAfter)
			{
				if (o instanceof commentType)
				{
					commentType commentType = (commentType) o;
					temp.getSpecialsAfter().add(commentType.createCopy(copyComments));
				}
			}
		}
		return temp;
	}

	public String toString()
	{
		StringBuffer sb = new StringBuffer("NameTok[");
		sb.append("id=");
		sb.append(dumpThis(this.id));
		sb.append(", ");
		sb.append("ctx=");
		sb.append(dumpThis(this.ctx, name_contextType.name_contextTypeNames));
		sb.append("]");
		return sb.toString();
	}

	public Object accept(VisitorIF visitor) throws Exception
	{
		return visitor.visitNameTok(this);
	}

	public void traverse(VisitorIF visitor) throws Exception
	{
	}

}
