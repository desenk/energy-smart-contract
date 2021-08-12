function a = Compute_Price_to_Pay(buyerarray,sellerarray)
a = mean(buyerarray(1),sellerarray(2))*min(buyerarray(2)*sellerarray(2));
end

