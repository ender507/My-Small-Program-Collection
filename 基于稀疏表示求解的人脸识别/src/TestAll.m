function TestAll(A)
    total_right = 0;
    total_wrong = 0;
    ROC = zeros(50, 4);    % 分别记录50个类的TP、TN、FP、FN值
    [total_right, total_wrong, ROC] = test('Alejandro_Toledo', 1, 39, ROC, total_right, total_wrong, A);
    [total_right, total_wrong, ROC] = test('Alvaro_Uribe', 2, 35, ROC, total_right, total_wrong, A);
    [total_right, total_wrong, ROC] = test('Andre_Agassi', 3, 36, ROC, total_right, total_wrong, A);
    [total_right, total_wrong, ROC] = test('Ariel_Sharon', 4, 40, ROC, total_right, total_wrong, A);
    [total_right, total_wrong, ROC] = test('Arnold_Schwarzenegger', 5, 40, ROC, total_right, total_wrong, A);
    [total_right, total_wrong, ROC] = test('Atal_Bihari_Vajpayee', 6, 24, ROC, total_right, total_wrong, A);
    [total_right, total_wrong, ROC] = test('Bill_Clinton', 7, 29, ROC, total_right, total_wrong, A);
    [total_right, total_wrong, ROC] = test('Colin_Powell', 8, 40, ROC, total_right, total_wrong, A);
    [total_right, total_wrong, ROC] = test('David_Beckham', 9, 31, ROC, total_right, total_wrong, A);
    [total_right, total_wrong, ROC] = test('Donald_Rumsfeld', 10, 40, ROC, total_right, total_wrong, A);
    [total_right, total_wrong, ROC] = test('George_Robertson', 11, 22, ROC, total_right, total_wrong, A);
    [total_right, total_wrong, ROC] = test('George_W_Bush', 12, 40, ROC, total_right, total_wrong, A);
    [total_right, total_wrong, ROC] = test('Gerhard_Schroeder', 13, 40, ROC, total_right, total_wrong, A);
    [total_right, total_wrong, ROC] = test('Gloria_Macapagal_Arroyo', 14, 40, ROC, total_right, total_wrong, A);
    [total_right, total_wrong, ROC] = test('Gray_Davis', 15, 26, ROC, total_right, total_wrong, A);
    [total_right, total_wrong, ROC] = test('Guillermo_Coria', 16, 30, ROC, total_right, total_wrong, A);
    [total_right, total_wrong, ROC] = test('Hamid_Karzai', 17, 22, ROC, total_right, total_wrong, A);
    [total_right, total_wrong, ROC] = test('Hans_Blix', 18, 39, ROC, total_right, total_wrong, A);
    [total_right, total_wrong, ROC] = test('Hugo_Chavez', 19, 40, ROC, total_right, total_wrong, A);
    [total_right, total_wrong, ROC] = test('Jack_Straw', 20, 28, ROC, total_right, total_wrong, A);
    [total_right, total_wrong, ROC] = test('Jacques_Chirac', 21, 40, ROC, total_right, total_wrong, A);
    [total_right, total_wrong, ROC] = test('Jean_Chretien', 22, 40, ROC, total_right, total_wrong, A);
    [total_right, total_wrong, ROC] = test('Jennifer_Capriati', 23, 40, ROC, total_right, total_wrong, A);
    [total_right, total_wrong, ROC] = test('Jeremy_Greenstock', 24, 24, ROC, total_right, total_wrong, A);
    [total_right, total_wrong, ROC] = test('John_Ashcroft', 25, 40, ROC, total_right, total_wrong, A);
    [total_right, total_wrong, ROC] = test('John_Negroponte', 26, 31, ROC, total_right, total_wrong, A);
    [total_right, total_wrong, ROC] = test('Jose_Maria_Aznar', 27, 23, ROC, total_right, total_wrong, A);
    [total_right, total_wrong, ROC] = test('Juan_Carlos_Ferrero', 28, 28, ROC, total_right, total_wrong, A);
    [total_right, total_wrong, ROC] = test('Junichiro_Koizumi', 29, 40, ROC, total_right, total_wrong, A);
    [total_right, total_wrong, ROC] = test('Kofi_Annan', 30, 32, ROC, total_right, total_wrong, A);
    [total_right, total_wrong, ROC] = test('Laura_Bush', 31, 40, ROC, total_right, total_wrong, A);
    [total_right, total_wrong, ROC] = test('Lleyton_Hewitt', 32, 40, ROC, total_right, total_wrong, A);
    [total_right, total_wrong, ROC] = test('Luiz_Inacio_Lula_da_Silva', 33, 40, ROC, total_right, total_wrong, A);
    [total_right, total_wrong, ROC] = test('Mahmoud_Abbas', 34, 29, ROC, total_right, total_wrong, A);
    [total_right, total_wrong, ROC] = test('Megawati_Sukarnoputri', 35, 33, ROC, total_right, total_wrong, A);
    [total_right, total_wrong, ROC] = test('Nestor_Kirchner', 36, 37, ROC, total_right, total_wrong, A);
    [total_right, total_wrong, ROC] = test('Recep_Tayyip_Erdogan', 37, 30, ROC, total_right, total_wrong, A);
    [total_right, total_wrong, ROC] = test('Ricardo_Lagos', 38, 27, ROC, total_right, total_wrong, A);
    [total_right, total_wrong, ROC] = test('Roh_Moo-hyun', 39, 32, ROC, total_right, total_wrong, A);
    [total_right, total_wrong, ROC] = test('Rudolph_Giuliani', 40, 26, ROC, total_right, total_wrong, A);
    [total_right, total_wrong, ROC] = test('Saddam_Hussein', 41, 23, ROC, total_right, total_wrong, A);
    [total_right, total_wrong, ROC] = test('Serena_Williams', 42, 40, ROC, total_right, total_wrong, A);
    [total_right, total_wrong, ROC] = test('Silvio_Berlusconi', 43, 33, ROC, total_right, total_wrong, A);
    [total_right, total_wrong, ROC] = test('Tiger_Woods', 44, 23, ROC, total_right, total_wrong, A);
    [total_right, total_wrong, ROC] = test('Tom_Daschle', 45, 25, ROC, total_right, total_wrong, A);
    [total_right, total_wrong, ROC] = test('Tom_Ridge', 46, 33, ROC, total_right, total_wrong, A);
    [total_right, total_wrong, ROC] = test('Tony_Blair', 47, 40, ROC, total_right, total_wrong, A);
    [total_right, total_wrong, ROC] = test('Vicente_Fox', 48, 32, ROC, total_right, total_wrong, A);
    [total_right, total_wrong, ROC] = test('Vladimir_Putin', 49, 40, ROC, total_right, total_wrong, A);
    [total_right, total_wrong, ROC] = test('Winona_Ryder', 50, 24, ROC, total_right, total_wrong, A);
    disp(total_right);
    disp(total_wrong);
    total = sum(sum(ROC(:,:)));
    disp(sum(ROC(:,1)) / total);
    disp(sum(ROC(:,2)) / total);
    disp(sum(ROC(:,3)) / total);
    disp(sum(ROC(:,4)) / total);
end

function [total_right, total_wrong, ROC] = test(name, id, num, ROC, total_right, total_wrong, A)
    right = 0;
    wrong = 0;
    row_range = 96:175;
    col_range = 101:160;
    row = 16; 
    col = 12;
    % 对当前类别下遍历所有测试图片
    for i = 21:num
        % 进行图片预处理
        test_img = imread(['test_set/', name, '/', name, '_00', num2str(i), '.jpg']); 
        test_img = im2double(test_img); % 灰度图化
        test_img = im2gray(test_img(row_range, col_range)); % 裁剪出面部     
        test_img = imresize(test_img,[row, col],'bilinear');  % 二线性差值下采样
        test_img = reshape(test_img, [row * col, 1]);    % 列向量化
        test_img = test_img / norm(test_img);
        % 进行分类
        x = BP_linprog(test_img, A);
        r = zeros(50,1);
        for j = 1:50
            delta_x = zeros(1000, 1);
            delta_x((j-1)*20+1 : j*20) = x((j-1)*20+1 : j*20);
            r(j) = norm(test_img - A * delta_x, 2);
        end
        % 得到类别后依据对错来更新统计信息
        for j = 1:50
            if r(j) == min(min(r))
                % 若分类正确
                if j == id
                    right = right + 1;
                    for k = 1:50
                        % 本类的TP+1
                       if k == id
                           ROC(k, 1) = ROC(k, 1) + 1;
                       % 其他类的TN+1
                       else
                           ROC(k, 2) = ROC(k, 2) + 1;
                       end
                    end
                % 若分类错误
                else
                    wrong = wrong + 1;
                    for k = 1:50
                        % 所属类的FN+1
                        if k == id
                            ROC(k, 4) = ROC(k, 4) + 1;
                        % 被分到的类的FP+1
                        elseif k == j
                            ROC(k, 3) = ROC(k, 3) + 1;
                        % 其他类的TN+1
                        else    
                            ROC(k, 2) = ROC(k, 2) + 1;
                        end
                    end
                end
                break
            end
        end
    end
    total_right = total_right + right;
    total_wrong = total_wrong + wrong;
end