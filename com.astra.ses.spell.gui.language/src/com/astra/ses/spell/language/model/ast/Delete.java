// Autogenerated AST node
package com.astra.ses.spell.language.model.ast;

import com.astra.ses.spell.language.model.SimpleNode;
import java.util.Arrays;

public final class Delete extends stmtType {
    public exprType[] targets;

    public Delete(exprType[] targets) {
        this.targets = targets;
    }

    public int hashCode() {
        final int prime = 31;
        int result = 1;
        result = prime * result + Arrays.hashCode(targets);
        return result;
    }

    public boolean equals(Object obj) {
        if (this == obj)
            return true;
        if (obj == null)
            return false;
        if (getClass() != obj.getClass())
            return false;
        Delete other = (Delete) obj;
        if (!Arrays.equals(targets, other.targets))
            return false;
        return true;
    }

    public Delete createCopy() {
        return createCopy(true);
    }

    public Delete createCopy(boolean copyComments) {
        exprType[] new0;
        if (this.targets != null) {
            new0 = new exprType[this.targets.length];
            for (int i = 0; i < this.targets.length; i++) {
                new0[i] = (exprType) (this.targets[i] != null ? this.targets[i].createCopy(copyComments) : null);
            }
        } else {
            new0 = this.targets;
        }
        Delete temp = new Delete(new0);
        temp.beginLine = this.beginLine;
        temp.beginColumn = this.beginColumn;
        if (this.specialsBefore != null && copyComments) {
            for (Object o : this.specialsBefore) {
                if (o instanceof commentType) {
                    commentType commentType = (commentType) o;
                    temp.getSpecialsBefore().add(commentType.createCopy(copyComments));
                }
            }
        }
        if (this.specialsAfter != null && copyComments) {
            for (Object o : this.specialsAfter) {
                if (o instanceof commentType) {
                    commentType commentType = (commentType) o;
                    temp.getSpecialsAfter().add(commentType.createCopy(copyComments));
                }
            }
        }
        return temp;
    }

    public String toString() {
        StringBuffer sb = new StringBuffer("Delete[");
        sb.append("targets=");
        sb.append(dumpThis(this.targets));
        sb.append("]");
        return sb.toString();
    }

    public Object accept(VisitorIF visitor) throws Exception {
        return visitor.visitDelete(this);
    }

    public void traverse(VisitorIF visitor) throws Exception {
        if (targets != null) {
            for (int i = 0; i < targets.length; i++) {
                if (targets[i] != null) {
                    targets[i].accept(visitor);
                }
            }
        }
    }

}