package main

import (
    "fmt"
    // "time"
    "math"
)

func main() {
    H,V := 512,512
    var n int
    var tmp float64
    max,max_k,max_L := 0.0,0,0.0
    max_o,max_k_o,max_L_o := 0.0,0,0.0
    fmt.Printf("Please input n:")
    fmt.Scanf("%d\n", &n)
    fmt.Printf("Please input H:")
    fmt.Scanf("%d\n", &H)
    fmt.Printf("Please input V:")
    fmt.Scanf("%d\n", &V)


    // Log2 testing
    // fmt.Printf("%f,",math.Log2(float64(2 * n + 1)))
    // fmt.Printf("%f,",math.Log2(4.0))
    // fmt.Printf("%f,",math.Log2(8.0))
    // fmt.Printf("%f\n",math.Log2(5.0))

    K := 1
    L := math.Floor(math.Log2(float64(2 * n + 1)))

    fmt.Println("Calculating ...")
    fmt.Println(" n     | K       | L       | max_k | max     | result")
    for K <= int(math.Floor(float64(H) * float64(V) / float64(n))) {
        tmp = math.Floor(math.Floor(float64(H * V / n)) / float64(K)) * L
        if tmp > max && L <= 64.0 {
            max_k = K
            max_L = L
            max = tmp
        }
        if tmp > max_o {
            max_k_o = K
            max_L_o = L
            max_o = tmp
        }
        fmt.Printf(" %-5d | %-7d | %-7.0f | %-5d | %-7.0f | %-.0f\n",n,K,L,max_k,max,tmp)
        K++
        L = math.Floor(float64(K) * math.Log2(float64(2 * n + 1)))
    }

    OPT := math.Log2(float64(2 * n + 1)) * math.Floor(float64(H * V / n))
    fmt.Printf("Affordable:\nMXC is %.0f, max_k: %d, max_L: %.0f, OPT: %f, CL: %f %%\n",max,max_k,max_L,OPT,(1.0 - float64(max) / OPT) * 100.0)
    fmt.Printf("Optimal:\nMXC is %.0f, max_k: %d, max_L: %.0f, OPT: %f, CL: %f %%\n",max_o,max_k_o,max_L_o,OPT,(1.0 - float64(max_o) / OPT) * 100.0)
}
