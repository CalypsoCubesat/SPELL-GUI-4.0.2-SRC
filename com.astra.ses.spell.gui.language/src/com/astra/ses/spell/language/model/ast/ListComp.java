// Autogenerated AST node
package com.astra.ses.spell.language.model.ast;

import com.astra.ses.spell.language.model.SimpleNode;
import java.util.Arrays;

public final class ListComp extends exprType implements comp_contextType {
    public exprType elt;
    public comprehensionType[] generators;
    public int ctx;

    public ListComp(exprType elt, comprehensionType[] generators, int ctx) {
        this.elt = elt;
        this.generators = generators;
        this.ctx = ctx;
    }

    public int hashCode() {
        final int prime = 31;
        int result = 1;
        result = prime * result + ((elt == null) ? 0 : elt.hashCode());
        result = prime * result + Arrays.hashCode(generators);
        result = prime * result + ctx;
        return result;
    }

    public boolean equals(Object obj) {
        if (this == obj)
            return true;
        if (obj == null)
            return false;
        if (getClass() != obj.getClass())
            return false;
        ListComp other = (ListComp) obj;
        if (elt == null) {
            if (other.elt != null)
                return false;
        } else if (!elt.equals(other.elt))
            return false;
        if (!Arrays.equals(generators, other.generators))
            return false;
        if (this.ctx != other.ctx)
            return false;
        return true;
    }

    public ListComp createCopy() {
        return createCopy(true);
    }

    public ListComp createCopy(boolean copyComments) {
        comprehensionType[] new0;
        if (this.generators != null) {
            new0 = new comprehensionType[this.generators.length];
            for (int i = 0; i < this.generators.length; i++) {
                new0[i] = (comprehensionType) (this.generators[i] != null ? this.generators[i].createCopy(copyComments)
                        : null);
            }
        } else {
            new0 = this.generators;
        }
        ListComp temp = new ListComp(elt != null ? (exprType) elt.createCopy(copyComments) : null, new0, ctx);
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
        StringBuffer sb = new StringBuffer("ListComp[");
        sb.append("elt=");
        sb.append(dumpThis(this.elt));
        sb.append(", ");
        sb.append("generators=");
        sb.append(dumpThis(this.generators));
        sb.append(", ");
        sb.append("ctx=");
        sb.append(dumpThis(this.ctx, comp_contextType.comp_contextTypeNames));
        sb.append("]");
        return sb.toString();
    }

    public Object accept(VisitorIF visitor) throws Exception {
        return visitor.visitListComp(this);
    }

    public void traverse(VisitorIF visitor) throws Exception {
        if (elt != null) {
            elt.accept(visitor);
        }
        if (generators != null) {
            for (int i = 0; i < generators.length; i++) {
                if (generators[i] != null) {
                    generators[i].accept(visitor);
                }
            }
        }
    }

}
