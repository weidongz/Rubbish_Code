function [valorAc, numZeros, numBits, EndOfBlock] = ACdecode(code)
    %decode AC catagory
    [runsize, codeLength_AC] = decode_category_AC(code);
    
    if (strcmp(runsize,'00'))
        EndOfBlock = boolean (1);
        valorAc = 0;
        numBits = 4;
        numZeros = 0;
    else
        EndOfBlock = boolean (0);
        category = (hex2dec(runsize(2)));
        numZeros = hex2dec(runsize(1));

        adBits = category;

        % Decode AC Value
        if (adBits == 0)
            decodeValorAc = 0;
        else
            if(code(codeLength_AC+1)=='0')
                for i=codeLength_AC+1:length(code)
                    if(code(i)=='1')
                        code(i)='0';
                    else
                        code(i)='1';
                    end
                end
                decodeValorAc = -bin2dec(code(codeLength_AC+1:codeLength_AC+adBits));
            else
                decodeValorAc = bin2dec(code(codeLength_AC+1:codeLength_AC+adBits));
            end            
        end

        valorAc = decodeValorAc;
        numBits = codeLength_AC + adBits;
    end
end