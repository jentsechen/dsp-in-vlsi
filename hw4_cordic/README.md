## To Do
* Q7
* Q8
* Q9
* Q10

## CORDIC Algorithm

$$\begin{bmatrix} X(i+1) \\ Y(i+1) \end{bmatrix} = \begin{bmatrix} \cos(\mu_i\theta_e(i)) & -\sin(\mu_i\theta_e(i)) \\ \sin(\mu_i\theta_e(i)) & \cos(\mu_i\theta_e(i)) \end{bmatrix} \begin{bmatrix} X(i) \\ Y(i) \end{bmatrix}$$

$$= \cos(\mu_i\theta_e(i)) \begin{bmatrix} 1 & -\mu_i 2^{-i} \\ \mu_i 2^{-i} & 1 \end{bmatrix} \begin{bmatrix} X(i) \\ Y(i) \end{bmatrix}$$

$$\text{where }\mu_i\in\{+1,-1\}\text{ and }\theta_e(i)=\tan^{-1}(2^{-i})$$

* Remark
    * $\frac{\sin(\mu_i\theta_e(i))}{\cos(\mu_i\theta_e(i))}=\tan(\mu_i\theta_e(i))=\tan(\mu_i\tan^{-1}(2^{-i}))=\mu_i\tan(\tan^{-1}(2^{-i}))=\mu_i 2^{-i}$
    * $\theta_e(i)$ is the elementary angle of the i-th micro-rotation