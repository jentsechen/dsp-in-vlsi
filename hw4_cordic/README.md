## To Do

## CORDIC Algorithm

$$\begin{bmatrix} X(i+1) \\ Y(i+1) \end{bmatrix} = \begin{bmatrix} \cos(\theta(i)) & -\sin(\theta(i)) \\ \sin(\theta(i)) & \cos(\theta(i)) \end{bmatrix} \begin{bmatrix} X(i) \\ Y(i) \end{bmatrix}$$

$$= \cos(\theta(i)) \begin{bmatrix} 1 & -\mu_i 2^{-i} \\ \mu_i 2^{-i} & 1 \end{bmatrix} \begin{bmatrix} X(i) \\ Y(i) \end{bmatrix}$$

$$\text{where }\mu_i\in\{+1,-1\}\text{ and }\theta(i)=\mu_i\tan^{-1}(2^{-i})$$

* Note: $\frac{\sin(\theta(i))}{\cos(\theta(i))}=\tan(\theta(i))=\tan(\mu_i\tan^{-1}(2^{-i}))=\mu_i\tan(\tan^{-1}(2^{-i}))=\mu_i 2^{-i}$