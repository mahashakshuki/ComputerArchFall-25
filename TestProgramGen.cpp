/******************************************************************************

Welcome to GDB Online.
  GDB online is an online compiler and debugger tool for C, C++, Python, PHP, Ruby, 
  C#, OCaml, VB, Perl, Swift, Prolog, Javascript, Pascal, COBOL, HTML, CSS, JS
  Code, Compile, Run and Debug online from anywhere in world.

*******************************************************************************/
#include <iostream>
#include <vector>
#include <string>
#include <random>

using namespace std;

// ---------------------------------------------------------
// Random number generator
// ---------------------------------------------------------
mt19937 rng(random_device{}());

int rand_int(int lo, int hi) {
    uniform_int_distribution<int> dist(lo, hi);
    return dist(rng);
}

string rand_reg() {
    return "x" + to_string(rand_int(0, 31));
}

int imm_i() { return rand_int(-2048, 2047); }
int imm_s() { return rand_int(-2048, 2047); }
int imm_j() { return rand_int(-2048, 2047); }
int imm_u() { return rand_int(0, 0xFFFFF) << 12; }

// ---------------------------------------------------------
// Instruction sets
// ---------------------------------------------------------
vector<string> R_TYPE = {
    "add", "sub", "and", "or", "xor",
    "sll", "srl", "sra", "slt", "sltu"
};

vector<string> I_TYPE = {
    "addi", "andi", "ori", "xori", "lw"
};

vector<string> S_TYPE = {"sw"};

vector<string> B_TYPE = {"beq", "bne"};

vector<string> U_TYPE = {"lui"};

vector<string> J_TYPE = {"jal"};

vector<string> ALL = {"R", "I", "S", "B", "U", "J"};

// ---------------------------------------------------------
// Generators
// ---------------------------------------------------------
string gen_r() {
    string op = R_TYPE[rand_int(0, R_TYPE.size() - 1)];
    return op + " " + rand_reg() + ", " + rand_reg() + ", " + rand_reg();
}

string gen_i() {
    string op = I_TYPE[rand_int(0, I_TYPE.size() - 1)];
    if (op == "lw")
        return "lw " + rand_reg() + ", " + to_string(imm_i()) + "(" + rand_reg() + ")";
    return op + " " + rand_reg() + ", " + rand_reg() + ", " + to_string(imm_i());
}

string gen_s() {
    return "sw " + rand_reg() + ", " + to_string(imm_s()) + "(" + rand_reg() + ")";
}

string gen_b(const string& L1, const string& L2) {
    string op = B_TYPE[rand_int(0, B_TYPE.size() - 1)];
    string lbl = (rand_int(0, 1) == 0 ? L1 : L2);
    return op + " " + rand_reg() + ", " + rand_reg() + ", " + lbl;
}

string gen_u() {
    return "lui " + rand_reg() + ", " + to_string(imm_u());
}

string gen_j(const string& L1) {
    return "jal " + rand_reg() + ", " + L1;
}

// ---------------------------------------------------------
// Program Generator
// ---------------------------------------------------------
vector<string> generate_program(int N) {
    vector<string> prog;

    string L1 = "L1";
    string L2 = "L2";

    prog.push_back(L1 + ":");

    for (int i = 0; i < N; i++) {
        string t = ALL[rand_int(0, ALL.size() - 1)];

        if (t == "R")      prog.push_back(gen_r());
        else if (t == "I") prog.push_back(gen_i());
        else if (t == "S") prog.push_back(gen_s());
        else if (t == "B") prog.push_back(gen_b(L1, L2));
        else if (t == "U") prog.push_back(gen_u());
        else if (t == "J") prog.push_back(gen_j(L1));
    }

    prog.push_back(L2 + ":");
    prog.push_back("addi x0, x0, 0   # end");

    return prog;
}

// ---------------------------------------------------------
// Main
// ---------------------------------------------------------
int main() {
    int N = 50; // number of random instructions

    vector<string> program = generate_program(N);

    for (auto& line : program) {
        cout << line << "\n";
    }

    return 0;
}
