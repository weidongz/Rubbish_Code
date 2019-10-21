function [valorDc numBits] = DCdecode(codeDC)
    %% decode DC category
    if (codeDC(1)=='0')
        if(codeDC(2)=='0')
            category = 0;
            adBits = 0;
            codeLength = 2;
        else
            if (codeDC(3)=='0')
                category = 1;
                adBits = 1;
                codeLength = 3;
            else
                category = 2;
                adBits = 2;
                codeLength = 3;
            end;
        end;
    else %codeDC(1)==1
        if(codeDC(2)=='0')
            if (codeDC(3)=='0');
                category = 3;
                adBits = 3;
                codeLength = 3;
            else
                category = 4;
                adBits = 4;
                codeLength = 3;
            end;
        else %codeDC(2)==1
            if(codeDC(3)=='0')
                category = 5;
                adBits = 5;
                codeLength = 3;
            else %codeDC(3)==1
                if(codeDC(4)=='0');
                    category = 6;
                    adBits = 6;
                    codeLength = 4;
                else %codeDC(4)==1
                    if(codeDC(5)=='0')
                        category = 7;
                        adBits = 7;
                        codeLength = 5;
                    else %codeDC(5)==1
                        if(codeDC(6)=='0')
                            category = 8;
                            adBits = 8;
                            codeLength = 6;
                        else %codeDC(6)==1
                            if(codeDC(7)=='0')
                                category = 9;
                                adBits = 9;
                                codeLength = 7;
                            else %codeDC(7)==1
                                if(codeDC(8)=='0')
                                    category = 10;
                                    adBits = 10;
                                    codeLength = 8;
                                else
                                    category = 11;
                                    adBits = 11;
                                    codeLength = 9;
                                end;
                            end;
                        end;
                    end;
                end;
            end;
        end;
    end;
    
    %% decode DC value
    if (adBits == 0)
        decodeValorDc = 0;
    else
        if(codeDC(codeLength+1)=='0')
            for i=codeLength+1:length(codeDC)
                if(codeDC(i)=='1')
                    codeDC(i)='0';
                else
                    codeDC(i)='1';
                end
            end
            decodeValorDc = -bin2dec(codeDC(codeLength+1:codeLength+adBits));
        else
            decodeValorDc = bin2dec(codeDC(codeLength+1:codeLength+adBits));
        end
        
    end
    
    valorDc = decodeValorDc;
    catDc = category;
    numBits = codeLength + adBits;
end
