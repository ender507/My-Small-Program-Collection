function  [A, class_name] = LoadTrainSet(row, col)
    A = zeros(row * col, 50 * 20); % 每个样本数据row * col维，共50类，每类20个样本
    class_name = {};                % 将类别编号与人脸姓名对应
    [A, class_name] = LoadOnePerson('Alejandro_Toledo', A, class_name, 0, row, col);
    [A, class_name] = LoadOnePerson('Alvaro_Uribe', A, class_name, 1, row, col);
    [A, class_name] = LoadOnePerson('Andre_Agassi', A, class_name, 2, row, col);
    [A, class_name] = LoadOnePerson('Ariel_Sharon', A, class_name, 3, row, col);
    [A, class_name] = LoadOnePerson('Arnold_Schwarzenegger', A, class_name, 4, row, col);
    [A, class_name] = LoadOnePerson('Atal_Bihari_Vajpayee', A, class_name, 5, row, col);
    [A, class_name] = LoadOnePerson('Bill_Clinton', A, class_name, 6, row, col);
    [A, class_name] = LoadOnePerson('Colin_Powell', A, class_name, 7, row, col);
    [A, class_name] = LoadOnePerson('David_Beckham', A, class_name, 8, row, col);
    [A, class_name] = LoadOnePerson('Donald_Rumsfeld', A, class_name, 9, row, col);
    [A, class_name] = LoadOnePerson('George_Robertson', A, class_name, 10, row, col);
    [A, class_name] = LoadOnePerson('George_W_Bush', A, class_name, 11, row, col);
    [A, class_name] = LoadOnePerson('Gerhard_Schroeder', A, class_name, 12, row, col);
    [A, class_name] = LoadOnePerson('Gloria_Macapagal_Arroyo', A, class_name, 13, row, col);
    [A, class_name] = LoadOnePerson('Gray_Davis', A, class_name, 14, row, col);
    [A, class_name] = LoadOnePerson('Guillermo_Coria', A, class_name, 15, row, col);
    [A, class_name] = LoadOnePerson('Hamid_Karzai', A, class_name, 16, row, col);
    [A, class_name] = LoadOnePerson('Hans_Blix', A, class_name, 17, row, col);
    [A, class_name] = LoadOnePerson('Hugo_Chavez', A, class_name, 18, row, col);
    [A, class_name] = LoadOnePerson('Jack_Straw', A, class_name, 19, row, col);
    [A, class_name] = LoadOnePerson('Jacques_Chirac', A, class_name, 20, row, col);
    [A, class_name] = LoadOnePerson('Jean_Chretien', A, class_name, 21, row, col);
    [A, class_name] = LoadOnePerson('Jennifer_Capriati', A, class_name, 22, row, col);
    [A, class_name] = LoadOnePerson('Jeremy_Greenstock', A, class_name, 23, row, col);
    [A, class_name] = LoadOnePerson('John_Ashcroft', A, class_name, 24, row, col);
    [A, class_name] = LoadOnePerson('John_Negroponte', A, class_name, 25, row, col);
    [A, class_name] = LoadOnePerson('Jose_Maria_Aznar', A, class_name, 26, row, col);
    [A, class_name] = LoadOnePerson('Juan_Carlos_Ferrero', A, class_name, 27, row, col);
    [A, class_name] = LoadOnePerson('Junichiro_Koizumi', A, class_name, 28, row, col);
    [A, class_name] = LoadOnePerson('Kofi_Annan', A, class_name, 29, row, col);
    [A, class_name] = LoadOnePerson('Laura_Bush', A, class_name, 30, row, col);
    [A, class_name] = LoadOnePerson('Lleyton_Hewitt', A, class_name, 31, row, col);
    [A, class_name] = LoadOnePerson('Luiz_Inacio_Lula_da_Silva', A, class_name, 32, row, col);
    [A, class_name] = LoadOnePerson('Mahmoud_Abbas', A, class_name, 33, row, col);
    [A, class_name] = LoadOnePerson('Megawati_Sukarnoputri', A, class_name, 34, row, col);
    [A, class_name] = LoadOnePerson('Nestor_Kirchner', A, class_name, 35, row, col);
    [A, class_name] = LoadOnePerson('Recep_Tayyip_Erdogan', A, class_name, 36, row, col);
    [A, class_name] = LoadOnePerson('Ricardo_Lagos', A, class_name, 37, row, col);
    [A, class_name] = LoadOnePerson('Roh_Moo-hyun', A, class_name, 38, row, col);
    [A, class_name] = LoadOnePerson('Rudolph_Giuliani', A, class_name, 39, row, col);
    [A, class_name] = LoadOnePerson('Saddam_Hussein', A, class_name, 40, row, col);
    [A, class_name] = LoadOnePerson('Serena_Williams', A, class_name, 41, row, col);
    [A, class_name] = LoadOnePerson('Silvio_Berlusconi', A, class_name, 42, row, col);
    [A, class_name] = LoadOnePerson('Tiger_Woods', A, class_name, 43, row, col);
    [A, class_name] = LoadOnePerson('Tom_Daschle', A, class_name, 44, row, col);
    [A, class_name] = LoadOnePerson('Tom_Ridge', A, class_name, 45, row, col);
    [A, class_name] = LoadOnePerson('Tony_Blair', A, class_name, 46, row, col);
    [A, class_name] = LoadOnePerson('Vicente_Fox', A, class_name, 47, row, col);
    [A, class_name] = LoadOnePerson('Vladimir_Putin', A, class_name, 48, row, col);
    [A, class_name] = LoadOnePerson('Winona_Ryder', A, class_name, 49, row, col);
end

function [A, class_name] = LoadOnePerson(name, A, class_name, no, row, col)
    class_name(no+1) = {name};
    row_range = 96:175;
    col_range = 101:160;
    for i = 1:20
        if i<10
            img = imread(['train_set/',name,'/',name,'_000',num2str(i),'.jpg']);
        else
            img = imread(['train_set/',name,'/',name,'_00',num2str(i),'.jpg']);
        end
        img = im2double(img);
        img = im2gray(img(row_range, col_range));
        img = imresize(img,[row, col],'bilinear');
        img = reshape(img, [row * col, 1]);
        img = img / norm(img);
        A(:, 20 * no + i) = img;
    end
end