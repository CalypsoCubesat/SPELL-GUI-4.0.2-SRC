// Autogenerated AST node
package com.astra.ses.spell.language.model.ast;

import com.astra.ses.spell.language.model.SimpleNode;
import java.util.Arrays;

public final class ExtSlice extends sliceType {
    public sliceType[] dims;

    public ExtSlice(sliceType[] dims) {
        this.dims = dims;
    }

    public int hashCode() {
        final int prime = 31;
        int result = 1;
        result = prime * result + Arrays.hashCode(dims);
        return result;
    }

    public boolean equals(Object obj) {
        if (this == obj)
            return true;
        if (obj == null)
            return false;
        if (getClass() != obj.getClass())
            return false;
        ExtSlice other = (ExtSlice) obj;
        if (!Arrays.equals(dims, other.dims))
            return false;
        return true;
    }

    public ExtSlice createCopy() {
        return createCopy(true);
    }

    public ExtSlice createCopy(boolean copyComments) {
        sliceType[] new0;
        if (this.dims != null) {
            new0 = new sliceType[this.dims.length];
            for (int i = 0; i < this.dims.length; i++) {
                new0[i] = (sliceType) (this.dims[i] != null ? this.dims[i].createCopy(copyComments) : null);
            }
        } else {
            new0 = this.dims;
        }
        ExtSlice temp = new ExtSlice(new0);
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
        StringBuffer sb = new StringBuffer("ExtSlice[");
        sb.append("dims=");
        sb.append(dumpThis(this.dims));
        sb.append("]");
        return sb.toString();
    }

    public Object accept(VisitorIF visitor) throws Exception {
        return visitor.visitExtSlice(this);
    }

    public void traverse(VisitorIF visitor) throws Exception {
        if (dims != null) {
            for (int i = 0; i < dims.length; i++) {
                if (dims[i] != null) {
                    dims[i].accept(visitor);
                }
            }
        }
    }

}