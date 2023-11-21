#include<stdio.h>
#include<ctype.h>
#include<stdlib.h>
#include<limits.h>
#include <time.h>

typedef unsigned long long ull;
typedef long long ll;

void wypiszBinarnie(ull n, ull m){
    for(ll i=n-1; i>=0; i--){
        printf("%llu", (m>>i)&1);
    }
    return;
}

int wczytajBinarne(ull *n){
    srand(time(NULL));
    int a;
    ull wartosc=0;
    int czyPoczatek=1;
    int czyWczytalismy=0;
    while(1){
        a=getchar();
        if(czyPoczatek && isspace(a) && a!=EOF){
            continue;
        }
        czyPoczatek=0;
        if(a!='1' && a!='0'){
            if(czyWczytalismy){
                ungetc(a, stdin);
                *n=wartosc;
                //printf("skuteczne wczytaniew\n");
                return 0;
            }
            return 1;
        }
        czyWczytalismy=1;
        wartosc<<=1;
        wartosc+=a-'0';
    }

}

ull generateNumber(ull n){
    ull r=rand();
    ull a=1<<n;
    a-=1;
    r&=a;
    return r;
}

ull generatePrzesuniecie(ull n){
    return rand()%(n+1);
}

ull makeOp(){
    return rand()%5;
}

int main(int argc, char *argv[]){
    srand (time(NULL));
    ull N;
    if(argc>2){
        printf("Niepoprawna ilość argumentów wywołania!\n");
        return 0;
    }
    else if(argc==2){
        N=atoi(argv[1]);
        if(N>sizeof(ull)*CHAR_BIT){
            printf("Za duży argument wywołania!\n");
            return 0;
        }
        if(N<=0){
            printf("Niedodatni argument wywołania!\n");
            return 0;
        }
    }
    else{
        N=8;
    }
    while(1){
        int o=makeOp();
        ull wynik;
        if(o<3){
            ull x=generateNumber(N);
            wypiszBinarnie(N, x);
            printf(" %llu\n", x);
            ull y=generateNumber(N);
            wypiszBinarnie(N, y);
            printf(" %llu\n", y);
            if(o==0){
                printf("operacja: &\n");
                wynik=x&y;
            }
            if(o==1){
                printf("operacja: |\n");
                wynik=x|y;
            }
            if(o==2){
                printf("operacja: ^\n");
                wynik=x^y;
            }
        }
        else{
            ull x=generateNumber(N);
            wypiszBinarnie(N, x);
            printf(" %llu\n", x);
            ull y=generatePrzesuniecie(N);
            printf("%llu\n", y);
            if(o==3){
                printf("operacja: <<\n");
                wynik=(x<<y)&((1<<N)-1);
            }
            if(o==4){
                printf("operacja: >> (przyjmij zera wiodace)\n");
                wynik=x>>y;
            }
        }
        ull guess;
        int czyKoniec=0;
        while(1){
            czyKoniec=wczytajBinarne(&guess);
            if(czyKoniec){
                break;
            }
            if(guess==wynik){
                printf("sukces\n");
                break;
            }
            else{
                printf("niepoprawnie\n");
            }
        }
        if(czyKoniec){
            break;
        }
    }
    printf("zakonczenie z powodu niebinarnego znaku lub EOF");
}
