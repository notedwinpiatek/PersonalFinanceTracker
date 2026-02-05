export const formatCurrency = (value, currencySign) => {
    const formatted = value.toLocaleString();
    return currencySign === "zł" ? `${formatted}${currencySign}` : `${currencySign}${formatted}`;
};