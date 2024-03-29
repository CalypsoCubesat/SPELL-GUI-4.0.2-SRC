// Autogenerated AST node
package com.astra.ses.spell.language.model.ast;

import com.astra.ses.spell.language.model.SimpleNode;
import java.util.Arrays;

public final class Compare extends exprType implements cmpopType {
    public exprType left;
    public int[] ops;
    public exprType[] comparators;

    public Compare(exprType left, int[] ops, exprType[] comparators) {
        this.left = left;
        this.ops = ops;
        this.comparators = comparators;
    }

    public int hashCode() {
        final int prime = 31;
        int result = 1;
        result = prime * result + ((left == null) ? 0 : left.hashCode());
        result = prime * result + Arrays.hashCode(ops);
        result = prime * result + Arrays.hashCode(comparators);
        return result;
    }

    public boolean equals(Object obj) {
        if (this == obj)
            return true;
        if (obj == null)
            return false;
        if (getClass() != obj.getClass())
            return false;
        Compare other = (Compare) obj;
        if (left == null) {
            if (other.left != null)
                return false;
        } else if (!left.equals(other.left))
            return false;
        if (!Arrays.equals(ops, other.ops))
            return false;
        if (!Arrays.equals(comparators, other.comparators))
            return false;
        return true;
    }

    public Compare createCopy() {
        return createCopy(true);
    }

    public Compare createCopy(boolean copyComments) {
        int[] new0;
        if (this.ops != null) {
            new0 = new int[this.ops.length];
            System.arraycopy(this.ops, 0, new0, 0, this.ops.length);
        } else {
            new0 = this.ops;
        }
        exprType[] new1;
        if (this.comparators != null) {
            new1 = new exprType[this.comparators.length];
            for (int i = 0; i < this.comparators.length; i++) {
                new1[i] = (exprType) (this.comparators[i] != null ? this.comparators[i].createCopy(copyComments) : null);
            }
        } else {
            new1 = this.comparators;
        }
        Compare temp = new Compare(left != null ? (exprType) left.createCopy(copyComments) : null, new0, new1);
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
        StringBuffer sb = new StringBuffer("Compare[");
        sb.append("left=");
        sb.append(dumpThis(this.left));
        sb.append(", ");
        sb.append("ops=");
        sb.append(dumpThis(this.ops, cmpopType.cmpopTypeNames));
        sb.append(", ");
        sb.append("comparators=");
        sb.append(dumpThis(this.comparators));
        sb.append("]");
        return sb.toString();
    }

    public Object accept(VisitorIF visitor) throws Exception {
        return visitor.visitCompare(this);
    }

    public void traverse(VisitorIF visitor) throws Exception {
        if (left != null) {
            left.accept(visitor);
        }
        if (comparators != null) {
            for (int i = 0; i < comparators.length; i++) {
                if (comparators[i] != null) {
                    comparators[i].accept(visitor);
                }
            }
        }
    }

}
