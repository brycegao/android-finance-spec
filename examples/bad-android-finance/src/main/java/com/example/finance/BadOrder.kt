package com.example.finance

import java.math.BigDecimal
import java.text.DecimalFormat
import kotlinx.coroutines.GlobalScope
import kotlinx.coroutines.launch

data class BadOrderDto(
    val amount: Double?,
    val price: Float?,
    val feeRate: Double?,
)

class BadOrderPresenter {
    fun bind(order: BadOrderDto?) {
        val total = order!!.amount!!.toDouble() * order.price!!.toDouble()
        val display = DecimalFormat("#,##0.00").format(total)
        val unsafeAmount = BigDecimal(order.amount)
        val unsafeStr = BigDecimal(order.amount).toString()

        GlobalScope.launch {
            println("total=$display unsafe=$unsafeAmount str=$unsafeStr")
        }
    }
}
