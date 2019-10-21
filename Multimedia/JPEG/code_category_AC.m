function [ code ] = code_category_AC( runsize )

% JPEG推荐的亮度交流霍夫曼编码表
% 输入AC系数中0行程长度以及非零所占比特数，
% 输出Huffman编码

    if (strcmp(runsize,'01'))
        code = '00';
    end
    
    if (strcmp(runsize,'02'))
        code = '01';
    end
    if (strcmp(runsize,'03'))
        code = '100';
    end
    if (strcmp(runsize,'04'))
        code = '1011';
    end
    if (strcmp(runsize,'05'))
        code = '11010';
    end
    if (strcmp(runsize,'06'))
        code = '1111000';
    end
    if (strcmp(runsize,'07'))
        code = '11111000';
    end
    if (strcmp(runsize,'08'))
        code = '1111110110';
    end
    if (strcmp(runsize,'09'))
        code = '1111111110000010';
    end
    if (strcmp(runsize,'0A'))
        code = '1111111110000011';
    end

    
    if (strcmp(runsize,'11'))
        code = '1100';
    end
    if (strcmp(runsize,'12'))
        code = '11011';
    end
    if (strcmp(runsize,'13'))
        code = '1111001';
    end
    if (strcmp(runsize,'14'))
        code = '111110110';
    end
    if (strcmp(runsize,'15'))
        code = '11111110110';
    end
    if (strcmp(runsize,'16'))
        code = '1111111110000100';
    end
    if (strcmp(runsize,'17'))
        code = '1111111110000101';
    end
    if (strcmp(runsize,'18'))
        code = '1111111110000110';
    end
    if (strcmp(runsize,'19'))
        code = '1111111110000111';
    end
    if (strcmp(runsize,'1A'))
        code = '1111111110001000';
    end

    if (strcmp(runsize,'21'))
        code = '11100';
    end
    if (strcmp(runsize,'22'))
        code = '11111001';
    end
    if (strcmp(runsize,'23'))
        code = '1111110111';
    end
    if (strcmp(runsize,'24'))
        code = '111111110100';
    end
    if (strcmp(runsize,'25'))
        code = '1111111110001001';
    end
    if (strcmp(runsize,'26'))
        code = '1111111110001010';
    end
    if (strcmp(runsize,'27'))
        code = '1111111110001011';
    end
    if (strcmp(runsize,'28'))
        code = '1111111110001100';
    end
    if (strcmp(runsize,'29'))
        code = '1111111110001101';
    end
    if (strcmp(runsize,'2A'))
        code = '1111111110001110';
    end

    if (strcmp(runsize,'31'))
        code = '111010';
    end
    if (strcmp(runsize,'32'))
        code = '111110111';
    end
    if (strcmp(runsize,'33'))
        code = '111111110101';
    end
    if (strcmp(runsize,'34'))
        code = '1111111110001111';
    end
    if (strcmp(runsize,'35'))
        code = '1111111110010000';
    end
    if (strcmp(runsize,'36'))
        code = '1111111110010001';
    end
    if (strcmp(runsize,'37'))
        code = '1111111110010010';
    end
    if (strcmp(runsize,'38'))
        code = '1111111110010011';
    end
    if (strcmp(runsize,'39'))
        code = '1111111110010100';
    end
    if (strcmp(runsize,'3A'))
        code = '1111111110010101';
    end

    if (strcmp(runsize,'41'))
        code = '111011';
    end
    if (strcmp(runsize,'42'))
        code = '1111111000';
    end
    if (strcmp(runsize,'43'))
        code = '1111111110010110';
    end
    if (strcmp(runsize,'44'))
        code = '1111111110010111';
    end
    if (strcmp(runsize,'45'))
        code = '1111111110011000';
    end
    if (strcmp(runsize,'46'))
        code = '1111111110011001';
    end
    if (strcmp(runsize,'47'))
        code = '1111111110011010';
    end
    if (strcmp(runsize,'48'))
        code = '1111111110011011';
    end
    if (strcmp(runsize,'49'))
        code = '1111111110011100';
    end
    if (strcmp(runsize,'4A'))
        code = '1111111110011101';
    end

    if (strcmp(runsize,'51'))
        code = '1111010';
    end
    if (strcmp(runsize,'52'))
        code = '11111110111';
    end
    if (strcmp(runsize,'53'))
        code = '1111111110011110';
    end
    if (strcmp(runsize,'54'))
        code = '1111111110011111';
    end
    if (strcmp(runsize,'55'))
        code = '1111111110100000';
    end
    if (strcmp(runsize,'56'))
        code = '1111111110100001';
    end
    if (strcmp(runsize,'57'))
        code = '1111111110100010';
    end
    if (strcmp(runsize,'58'))
        code = '1111111110100011';
    end
    if (strcmp(runsize,'59'))
        code = '1111111110100100';
    end
    if (strcmp(runsize,'5A'))
        code = '1111111110100101';
    end


    if (strcmp(runsize,'61'))
        code = '1111011';
    end
    if (strcmp(runsize,'62'))
        code = '111111110110';
    end
    if (strcmp(runsize,'63'))
        code = '1111111110100110';
    end
    if (strcmp(runsize,'64'))
        code = '1111111110100111';
    end
    if (strcmp(runsize,'65'))
        code = '1111111110101000';
    end
    if (strcmp(runsize,'66'))
        code = '1111111110101001';
    end
    if (strcmp(runsize,'67'))
        code = '1111111110101010';
    end
    if (strcmp(runsize,'68'))
        code = '1111111110101011';
    end
    if (strcmp(runsize,'69'))
        code = '1111111110101100';
    end
    if (strcmp(runsize,'6A'))
        code = '1111111110101101';
    end



    if (strcmp(runsize,'71'))
        code = '11111010';
    end
    if (strcmp(runsize,'72'))
        code = '111111110111';
    end
    if (strcmp(runsize,'73'))
        code = '1111111110101110';
    end
    if (strcmp(runsize,'74'))
        code = '1111111110101111';
    end
    if (strcmp(runsize,'75'))
        code = '1111111110110000';
    end
    if (strcmp(runsize,'76'))
        code = '1111111110110001';
    end
    if (strcmp(runsize,'77'))
        code = '1111111110110010';
    end
    if (strcmp(runsize,'78'))
        code = '1111111110110011';
    end
    if (strcmp(runsize,'79'))
        code = '1111111110110100';
    end
    if (strcmp(runsize,'7A'))
        code = '1111111110110101';
    end

    if (strcmp(runsize,'81'))
        code = '111111000';
    end
    if (strcmp(runsize,'82'))
        code = '111111111000000';
    end
    if (strcmp(runsize,'83'))
        code = '1111111110110110';
    end
    if (strcmp(runsize,'84'))
        code = '1111111110110111';
    end
    if (strcmp(runsize,'85'))
        code = '1111111110111000';
    end
    if (strcmp(runsize,'86'))
        code = '1111111110111001';
    end
    if (strcmp(runsize,'87'))
        code = '1111111110111010';
    end
    if (strcmp(runsize,'88'))
        code = '1111111110111011';
    end
    if (strcmp(runsize,'89'))
        code = '1111111110111100';
    end
    if (strcmp(runsize,'8A'))
        code = '1111111110111101';
    end



    if (strcmp(runsize,'91'))
        code = '111111001';
    end
    if (strcmp(runsize,'92'))
        code = '1111111110111110';
    end
    if (strcmp(runsize,'93'))
        code = '1111111110111111';
    end
    if (strcmp(runsize,'94'))
        code = '1111111111000000';
    end
    if (strcmp(runsize,'95'))
        code = '1111111111000001';
    end
    if (strcmp(runsize,'96'))
        code = '1111111111000010';
    end
    if (strcmp(runsize,'97'))
        code = '1111111111000011';
    end
    if (strcmp(runsize,'98'))
        code = '1111111111000100';
    end
    if (strcmp(runsize,'99'))
        code = '1111111111000101';
    end
    if (strcmp(runsize,'9A'))
        code = '1111111111000110';
    end


    if (strcmp(runsize,'A1'))
        code = '111111010';
    end
    if (strcmp(runsize,'A2'))
        code = '1111111111000111';
    end
    if (strcmp(runsize,'A3'))
        code = '1111111111001000';
    end
    if (strcmp(runsize,'A4'))
        code = '1111111111001001';
    end
    if (strcmp(runsize,'A5'))
        code = '1111111111001010';
    end
    if (strcmp(runsize,'A6'))
        code = '1111111111001011';
    end
    if (strcmp(runsize,'A7'))
        code = '1111111111001100';
    end
    if (strcmp(runsize,'A8'))
        code = '1111111111001101';
    end
    if (strcmp(runsize,'A9'))
        code = '1111111111001110';
    end
    if (strcmp(runsize,'AA'))
        code = '1111111111001111';
    end


    if (strcmp(runsize,'B1'))
        code = '1111111001';
    end
    if (strcmp(runsize,'B2'))
        code = '1111111111010000';
    end
    if (strcmp(runsize,'B3'))
        code = '1111111111010001';
    end
    if (strcmp(runsize,'B4'))
        code = '1111111111010010';
    end
    if (strcmp(runsize,'B5'))
        code = '1111111111010011';
    end
    if (strcmp(runsize,'B6'))
        code = '1111111111010100';
    end
    if (strcmp(runsize,'B7'))
        code = '1111111111010101';
    end
    if (strcmp(runsize,'B8'))
        code = '1111111111010110';
    end
    if (strcmp(runsize,'B9'))
        code = '1111111111010111';
    end
    if (strcmp(runsize,'BA'))
        code = '1111111111011000';
    end


    if (strcmp(runsize,'C1'))
        code = '1111111010';
    end
    if (strcmp(runsize,'C2'))
        code = '1111111111011001';
    end
    if (strcmp(runsize,'C3'))
        code = '1111111111011010';
    end
    if (strcmp(runsize,'C4'))
        code = '1111111111011011';
    end
    if (strcmp(runsize,'C5'))
        code = '1111111111011100';
    end
    if (strcmp(runsize,'C6'))
        code = '1111111111011101';
    end
    if (strcmp(runsize,'C7'))
        code = '1111111111011110';
    end
    if (strcmp(runsize,'C8'))
        code = '1111111111011111';
    end
    if (strcmp(runsize,'C9'))
        code = '1111111111100000';
    end
    if (strcmp(runsize,'CA'))
        code = '1111111111100001';
    end


    if (strcmp(runsize,'D1'))
        code = '11111111000';
    end
    if (strcmp(runsize,'D2'))
        code = '1111111111100010';
    end
    if (strcmp(runsize,'D3'))
        code = '1111111111100011';
    end
    if (strcmp(runsize,'D4'))
        code = '1111111111100100';
    end
    if (strcmp(runsize,'D5'))
        code = '1111111111100101';
    end
    if (strcmp(runsize,'D6'))
        code = '1111111111100110';
    end
    if (strcmp(runsize,'D7'))
        code = '1111111111100111';
    end
    if (strcmp(runsize,'D8'))
        code = '1111111111101000';
    end
    if (strcmp(runsize,'D9'))
        code = '1111111111101001';
    end
    if (strcmp(runsize,'DA'))
        code = '1111111111101010';
    end


    if (strcmp(runsize,'E1'))
        code = '1111111111101011';
    end
    if (strcmp(runsize,'E2'))
        code = '1111111111101100';
    end
    if (strcmp(runsize,'E3'))
        code = '1111111111101101';
    end
    if (strcmp(runsize,'E4'))
        code = '1111111111101110';
    end
    if (strcmp(runsize,'E5'))
        code = '1111111111101111';
    end
    if (strcmp(runsize,'E6'))
        code = '1111111111110000';
    end
    if (strcmp(runsize,'E7'))
        code = '1111111111110001';
    end
    if (strcmp(runsize,'E8'))
        code = '1111111111110010';
    end
    if (strcmp(runsize,'E9'))
        code = '1111111111110011';
    end
    if (strcmp(runsize,'EA'))
        code = '1111111111110100';
    end


    if (strcmp(runsize,'F0'))
        code = '11111111001';
    end
    if (strcmp(runsize,'F1'))
        code = '1111111111110101';
    end
    if (strcmp(runsize,'F2'))
        code = '1111111111110110';
    end
    if (strcmp(runsize,'F3'))
        code = '1111111111110111';  
    end
    if (strcmp(runsize,'F4'))
        code = '1111111111111000';
    end
    if (strcmp(runsize,'F5'))
        code = '1111111111111001';
    end
    if (strcmp(runsize,'F6'))
        code = '1111111111111010';
    end
    if (strcmp(runsize,'F7'))
        code = '1111111111111011';
    end
    if (strcmp(runsize,'F8'))
        code = '1111111111111100';
    end
    if (strcmp(runsize,'F9'))
        code = '1111111111111101';
    end
    if (strcmp(runsize,'FA'));
        code = '1111111111111110'   
    end

end

