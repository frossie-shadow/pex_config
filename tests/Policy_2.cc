/**
 * @file Policy_2.cc
 *
 * This test tests the format-specific parsers for Policies.  
 */
#include <sstream>
#include <fstream>
#include <string>
#include <stdexcept>
#include <list>
#include "lsst/pex/policy/json/JSONParser.h"
#include "lsst/pex/policy/paf/PAFParser.h"
#include "lsst/pex/policy/Policy.h"

using namespace std;
using lsst::pex::policy::Policy;
using lsst::pex::policy::paf::PAFParser;
using lsst::pex::policy::json::JSONParser;
using lsst::pex::policy::TypeError;
using lsst::pex::policy::NameNotFound;

#define Assert(b, m) tattle(b, m, __LINE__)

void tattle(bool mustBeTrue, const string& failureMsg, int line) {
    if (! mustBeTrue) {
        ostringstream msg;
        msg << __FILE__ << ':' << line << ":\n" << failureMsg << ends;
        throw runtime_error(msg.str());
    }
}

int main(int argc, char** argv) {

    Policy p1;
    JSONParser jp(p1);
    cout << "the JSON parser will" << ((jp.isStrict()) ? " " : " not ")
         << "be strict.\n"         << endl;

    ifstream is("examples/EventTranmitter_policy.json");

    jp.parse(is);
    is.close();

    cout << "Contents of JSON file:" << endl;
    cout << p1 << endl;

    string dataerror("Incorrect data found for ");
    Assert(p1.getString("receiver.logVerbosity") == "debug", 
           dataerror+"receiver.logVerbosity");
    Assert(p1.getString("transmitter.logVerbosity") == "debug", 
           dataerror+"transmitter.logVerbosity");
    Assert(p1.getString("transmitter.serializationFormat") == "deluxe", 
           dataerror+"transmitter.serializationFormat");
    Assert(p1.getBool("standalone"), dataerror+"standalone");
    Assert(p1.getDouble("threshold") == 4.5, dataerror+"threshold");

    Policy p2;
    PAFParser pp(p2);
    is.open("examples/EventTranmitter_policy.paf");

    pp.parse(is);

    cout << "Contents of PAF file:" << endl;
    cout << p2 << endl;

    Assert(p2.getString("receiver.logVerbosity") == "debug", 
           dataerror+"receiver.logVerbosity");
    Assert(p2.getString("transmitter.logVerbosity") == "debug", 
           dataerror+"transmitter.logVerbosity");
    Assert(p2.getString("transmitter.serializationFormat") == "deluxe", 
           dataerror+"transmitter.serializationFormat");
    Assert(p2.getBool("standalone"), dataerror+"standalone");
    Assert(p2.getDouble("threshold") == 4.5, dataerror+"threshold");

//     list<string> names;
//     p.paramNames(names);

//     for(list<string>::iterator i=names.begin(); i!=names.end(); ++i) 
//         cout << *i << endl;

}