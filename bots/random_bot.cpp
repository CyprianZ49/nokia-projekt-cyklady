// Tries to recruit philosophers if possible, otherwise bets for apollo.

#include <bits/stdc++.h>

using namespace std;

void do_move()
{
    string info;
    while(info!="-2") // waits for its turn
        cin>>info;
    vector<string> all_moves;
    string moves;
    getline(cin,moves);
    unsigned int l=0;
    while(l<moves.size())
    {
        int r=moves.find("|", l);
        if(r==-1)
            break;
        all_moves.push_back(moves.substr(l,r-l));
        l=r+1;
    }
    cout<<all_moves[rand()%all_moves.size()]<<endl;
}

int main()
{
    while(true)
        do_move();
}