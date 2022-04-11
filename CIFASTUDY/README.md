## Installation

```conda 
    conda install -c anaconda keras
```


## Layer class : 네트워크에서의 레이어의 추상화된 클래스 
### KERAS CAN"T DO 
    1. gradients
    2. device placements
    3. 분산 학습
    4. N개 샘플의 텐서로 시작하지 않는 것
    5. 타입 체크 

### Things I store to get used to.
```python
    return cifar_train_data, cifar_train_filenames, cifar_train_labels, \
        cifar_test_data, cifar_test_filenames, cifar_test_labels, cifar_label_names
    # In this way, \ helps us to understand that the above code is the same as cifar_train_data, cifar_train_filenames, cifar_train_labels, cifar_test_data, cifar_test_filenames, cifar_test_labels, cifar_label_names("줄바꿈으로 인식 - 너무 길어서 임의로 보기 쉽게 \ 로 표현")
```