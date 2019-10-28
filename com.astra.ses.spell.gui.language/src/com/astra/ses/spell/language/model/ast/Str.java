// Autogenerated AST node
package com.astra.ses.spell.language.model.ast;

import com.astra.ses.spell.language.model.SimpleNode;
import java.util.Arrays;

public final class Str extends exprType implements str_typeType {
    public String s;
    public int type;
    public boolean unicode;
    public boolean raw;
    public boolean binary;

    public Str(String s, int type, boolean unicode, boolean raw, boolean binary) {
        this.s = s;
        this.type = type;
        this.unicode = unicode;
        this.raw = raw;
        this.binary = binary;
    }

    public int hashCode() {
        final int prime = 31;
        int result = 1;
        result = prime * result + ((s == null) ? 0 : s.hashCode());
        result = prime * result + type;
        result = prime * result + (unicode ? 17 : 137);
        result = prime * result + (raw ? 17 : 137);
        result = prime * result + (binary ? 17 : 137);
        return result;
    }

    public boolean equals(Object obj) {
        if (this == obj)
            return true;
        if (obj == null)
            return false;
        if (getClass() != obj.getClass())
            return false;
        Str other = (Str) obj;
        if (s == null) {
            if (other.s != null)
                return false;
        } else if (!s.equals(other.s))
            return false;
        if (this.type != other.type)
            return false;
        if (this.unicode != other.unicode)
            return false;
        if (this.raw != other.raw)
            return false;
        if (this.binary != other.binary)
            return false;
        return true;
    }

    public Str createCopy() {
        return createCopy(true);
    }

    public Str createCopy(boolean copyComments) {
        Str temp = new Str(s, type, unicode, raw, binary);
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
        StringBuffer sb = new StringBuffer("Str[");
        sb.append("s=");
        sb.append(dumpThis(this.s));
        sb.append(", ");
        sb.append("type=");
        sb.append(dumpThis(this.type, str_typeType.str_typeTypeNames));
        sb.append(", ");
        sb.append("unicode=");
        sb.append(dumpThis(this.unicode));
        sb.append(", ");
        sb.append("raw=");
        sb.append(dumpThis(this.raw));
        sb.append(", ");
        sb.append("binary=");
        sb.append(dumpThis(this.binary));
        sb.append("]");
        return sb.toString();
    }

    public Object accept(VisitorIF visitor) throws Exception {
        return visitor.visitStr(this);
    }

    public void traverse(VisitorIF visitor) throws Exception {
    }

}
