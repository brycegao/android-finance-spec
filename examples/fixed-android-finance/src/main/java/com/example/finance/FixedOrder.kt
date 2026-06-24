package com.example.finance

import java.math.BigDecimal
import kotlinx.coroutines.CoroutineScope
import kotlinx.coroutines.launch

data class FixedOrderDto(
    val amount: String?,
    val price: String?,
    val feeRate: String?,
)

class FixedOrderPresenter(
    private val scope: CoroutineScope,
) {
    fun bind(order: FixedOrderDto) {
        val total = order.amount.multiplyBy(order.price)
        val display = NumericFormat.format(total, digit = 2)
        val plainStr = total.toPlainString()

        scope.launch {
            println("total=$display")
        }
    }

    private fun String?.multiplyBy(other: String?): String? {
        val left = this?.toBigDecimalOrNull() ?: return null
        val right = other?.toBigDecimalOrNull() ?: return null
        return left.multiply(right).stripTrailingZeros().toPlainString()
    }
}

object NumericFormat {
    fun format(value: String?, digit: Int): String {
        val decimal = value?.toBigDecimalOrNull() ?: return "--"
        return decimal.setScale(digit, java.math.RoundingMode.DOWN).toPlainString()
    }
}
