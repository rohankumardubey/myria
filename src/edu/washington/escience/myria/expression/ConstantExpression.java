package edu.washington.escience.myria.expression;

import java.util.Objects;

import org.apache.commons.lang.StringEscapeUtils;
import org.joda.time.DateTime;

import com.fasterxml.jackson.annotation.JsonProperty;

import edu.washington.escience.myria.Type;
import edu.washington.escience.myria.expression.evaluate.ExpressionOperatorParameter;

/**
 * An expression that returns a constant value.
 */
public class ConstantExpression extends ZeroaryExpression {

  /***/
  private static final long serialVersionUID = 1L;

  /** The type of this object. */
  @JsonProperty
  private final Type valueType;

  /** The value of this object. */
  @JsonProperty
  private final String value;

  /**
   * This is not really unused, it's used automagically by Jackson deserialization.
   */
  @SuppressWarnings("unused")
  private ConstantExpression() {
    valueType = null;
    value = null;
  }

  /**
   * @param type the type of this object.
   * @param value the value of this constant.
   */
  public ConstantExpression(final Type type, final String value) {
    valueType = type;
    this.value = value;
  }

  /**
   * Construct integer constant.
   * 
   * @param value the value of this constant.
   */
  public ConstantExpression(final int value) {
    valueType = Type.INT_TYPE;
    this.value = String.valueOf(value);
  }

  /**
   * Construct long constant.
   * 
   * @param value the value of this constant.
   */
  public ConstantExpression(final long value) {
    valueType = Type.LONG_TYPE;
    this.value = String.valueOf(value);
  }

  /**
   * Construct float constant.
   * 
   * @param value the value of this constant.
   */
  public ConstantExpression(final float value) {
    valueType = Type.FLOAT_TYPE;
    this.value = String.valueOf(value) + "f";
  }

  /**
   * Construct double constant.
   * 
   * @param value the value of this constant.
   */
  public ConstantExpression(final double value) {
    valueType = Type.DOUBLE_TYPE;
    this.value = String.valueOf(value);
  }

  /**
   * Construct boolean constant.
   * 
   * @param value the value of this constant.
   */
  public ConstantExpression(final boolean value) {
    valueType = Type.BOOLEAN_TYPE;
    this.value = String.valueOf(value);
  }

  /**
   * Construct datetime constant.
   * 
   * @param value the value of this constant.
   */
  public ConstantExpression(final DateTime value) {
    valueType = Type.DATETIME_TYPE;
    this.value = String.valueOf(value);
  }

  @Override
  public Type getOutputType(final ExpressionOperatorParameter parameters) {
    return valueType;
  }

  @Override
  public String getJavaString(final ExpressionOperatorParameter parameters) {
    switch (valueType) {
      case BOOLEAN_TYPE:
      case DOUBLE_TYPE:
      case FLOAT_TYPE:
      case INT_TYPE:
      case LONG_TYPE:
        return value;
      case DATETIME_TYPE:
        throw new UnsupportedOperationException("using constant value of type DateTime");
      case STRING_TYPE:
        return '\"' + StringEscapeUtils.escapeJava(value) + '\"';
    }
    throw new UnsupportedOperationException("using constant value of type " + valueType);
  }

  @Override
  public int hashCode() {
    return Objects.hash(getClass().getCanonicalName(), valueType, value);
  }

  @Override
  public boolean equals(final Object other) {
    if (other == null || !(other instanceof ConstantExpression)) {
      return false;
    }
    ConstantExpression otherExp = (ConstantExpression) other;
    return Objects.equals(valueType, otherExp.valueType) && Objects.equals(value, otherExp.value);
  }

  /**
   * @return the value
   */
  public String getValue() {
    return value;
  }
}
